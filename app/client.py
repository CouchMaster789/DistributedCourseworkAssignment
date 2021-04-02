import asyncio
import logging

import grpc

from app import matrix_computations_pb2, matrix_computations_pb2_grpc
from app.utils import encode_matrix, decode_matrix


async def run(matrix_1, matrix_2):
    matrix_length = len(matrix_1)
    b_size = 2

    a1, a2, b1, b2, c1, c2, d1, d2 = get_matrix_partials(matrix_length, b_size, matrix_1, matrix_2)

    channels = [grpc.aio.insecure_channel(f'localhost:{port}') for port in range(50052, 50054)]
    stubs = [matrix_computations_pb2_grpc.ComputerStub(channel) for channel in channels]

    a3_1, a3_2, b3_1, b3_2, c3_1, c3_2, d3_1, d3_2 = await asyncio.gather(
        stubs[0].multiply_block(prepare_data(a1, a2)),
        stubs[0].multiply_block(prepare_data(b1, c2)),
        stubs[0].multiply_block(prepare_data(a1, b2)),
        stubs[0].multiply_block(prepare_data(b1, d2)),
        stubs[1].multiply_block(prepare_data(c1, a2)),
        stubs[1].multiply_block(prepare_data(d1, c2)),
        stubs[1].multiply_block(prepare_data(c1, b2)),
        stubs[1].multiply_block(prepare_data(d1, d2))
    )

    a3, b3, c3, d3 = await asyncio.gather(
        stubs[0].add_block(prepare_data(decode_matrix(a3_1.matrix), decode_matrix(a3_2.matrix))),
        stubs[0].add_block(prepare_data(decode_matrix(b3_1.matrix), decode_matrix(b3_2.matrix))),
        stubs[1].add_block(prepare_data(decode_matrix(c3_1.matrix), decode_matrix(c3_2.matrix))),
        stubs[1].add_block(prepare_data(decode_matrix(d3_1.matrix), decode_matrix(d3_2.matrix))),
    )

    result = construct_result(matrix_length, b_size, decode_matrix(a3.matrix), decode_matrix(b3.matrix),
                              decode_matrix(c3.matrix), decode_matrix(d3.matrix))

    print(result)
    return result


def prepare_data(matrix_a, matrix_b):
    return matrix_computations_pb2.ComputationRequest(matrix_1=encode_matrix(matrix_a),
                                                      matrix_2=encode_matrix(matrix_b))


def get_matrix_partials(matrix_length, b_size, matrix_1, matrix_2):
    partials = [[[0 for _ in range(matrix_length)] for _ in range(matrix_length)] for _ in range(8)]

    for i in range(b_size):
        for j in range(b_size):
            partials[0][i][j] = matrix_1[i][j]
            partials[1][i][j] = matrix_2[i][j]

    for i in range(b_size):
        for j in range(b_size, matrix_length):
            partials[2][i][j - b_size] = matrix_1[i][j]
            partials[3][i][j - b_size] = matrix_2[i][j]

    for i in range(b_size, matrix_length):
        for j in range(b_size):
            partials[4][i - b_size][j] = matrix_1[i][j]
            partials[5][i - b_size][j] = matrix_2[i][j]

    for i in range(b_size, matrix_length):
        for j in range(b_size, matrix_length):
            partials[6][i - b_size][j - b_size] = matrix_1[i][j]
            partials[7][i - b_size][j - b_size] = matrix_2[i][j]

    return partials


def construct_result(matrix_length, b_size, a3, b3, c3, d3):
    result = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]

    for i in range(b_size):
        for j in range(b_size):
            result[i][j] = a3[i][j]

    for i in range(b_size):
        for j in range(b_size, matrix_length):
            result[i][j] = b3[i][j - b_size]

    for i in range(b_size, matrix_length):
        for j in range(b_size):
            result[i][j] = c3[i - b_size][j]

    for i in range(b_size, matrix_length):
        for j in range(b_size, matrix_length):
            result[i][j] = d3[i - b_size][j - b_size]

    return result


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run([[1, 2, 3, 4],
                     [5, 6, 7, 8],
                     [9, 10, 11, 12],
                     [13, 14, 15, 16]],
                    [[1, 2, 3, 4],
                     [5, 6, 7, 8],
                     [9, 10, 11, 12],
                     [13, 14, 15, 16]]))
