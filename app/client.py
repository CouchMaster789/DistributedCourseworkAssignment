import asyncio
import logging

import grpc
import numpy as np

from app import matrix_computations_pb2, matrix_computations_pb2_grpc
from app.utils import encode_matrix, decode_matrix


async def run(matrix_1, matrix_2):
    async with grpc.aio.insecure_channel('localhost:50052') as channel:
        stub = matrix_computations_pb2_grpc.ComputerStub(channel)

        prepare_data = lambda matrix_a, matrix_b: matrix_computations_pb2.ComputationRequest(
            matrix_1=encode_matrix(matrix_a),
            matrix_2=encode_matrix(matrix_b)
        )

        matrix_length = len(matrix_1)
        b_size = 2

        a1 = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]
        a2 = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]
        b1 = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]
        b2 = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]
        c1 = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]
        c2 = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]
        d1 = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]
        d2 = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]
        result = [[0 for _ in range(matrix_length)] for _ in range(matrix_length)]

        for i in range(b_size):
            for j in range(b_size):
                a1[i][j] = matrix_1[i][j]
                a2[i][j] = matrix_2[i][j]

        for i in range(b_size):
            for j in range(b_size, matrix_length):
                b1[i][j - b_size] = matrix_1[i][j]
                b2[i][j - b_size] = matrix_2[i][j]

        for i in range(b_size, matrix_length):
            for j in range(b_size):
                c1[i - b_size][j] = matrix_1[i][j]
                c2[i - b_size][j] = matrix_2[i][j]

        for i in range(b_size, matrix_length):
            for j in range(b_size, matrix_length):
                d1[i - b_size][j - b_size] = matrix_1[i][j]
                d2[i - b_size][j - b_size] = matrix_2[i][j]

        a3_1 = await stub.multiply_block(prepare_data(a1, a2))
        a3_2 = await stub.multiply_block(prepare_data(b1, c2))
        a3 = np.add(decode_matrix(a3_1.matrix), decode_matrix(a3_2.matrix))

        b3_1 = await stub.multiply_block(prepare_data(a1, b2))
        b3_2 = await stub.multiply_block(prepare_data(b1, d2))
        b3 = np.add(decode_matrix(b3_1.matrix), decode_matrix(b3_2.matrix))

        c3_1 = await stub.multiply_block(prepare_data(c1, a2))
        c3_2 = await stub.multiply_block(prepare_data(d1, c2))
        c3 = np.add(decode_matrix(c3_1.matrix), decode_matrix(c3_2.matrix))

        d3_1 = await stub.multiply_block(prepare_data(c1, b2))
        d3_2 = await stub.multiply_block(prepare_data(d1, d2))
        d3 = np.add(decode_matrix(d3_1.matrix), decode_matrix(d3_2.matrix))
        # d3 = stub.add_block(prepare_data(d3_1.matrix, d3_2.matrix)).matrix

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
