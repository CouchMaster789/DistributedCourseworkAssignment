from __future__ import print_function

import logging

import grpc
from app import matrix_computations_pb2, matrix_computations_pb2_grpc
from app.utils import encode_matrix, decode_matrix


def run(matrix_1, matrix_2):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = matrix_computations_pb2_grpc.ComputerStub(channel)

        multiply_block = lambda matrix_a, matrix_b: decode_matrix(
            stub.multiply_block(matrix_computations_pb2.ComputationRequest(
                matrix_1=encode_matrix(matrix_a), matrix_2=encode_matrix(matrix_b))
            ).matrix)

        add_block = lambda matrix_a, matrix_b: decode_matrix(stub.add_block(matrix_computations_pb2.ComputationRequest(
            matrix_1=encode_matrix(matrix_a), matrix_2=encode_matrix(matrix_b)
        )).matrix)

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

        a3 = add_block(multiply_block(a1, a2), multiply_block(b1, c2))
        b3 = add_block(multiply_block(a1, b2), multiply_block(b1, d2))
        c3 = add_block(multiply_block(c1, a2), multiply_block(d1, c2))
        d3 = add_block(multiply_block(c1, b2), multiply_block(d1, d2))

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
    run([[1, 2, 3, 4],
         [5, 6, 7, 8],
         [9, 10, 11, 12],
         [13, 14, 15, 16]],

        [[1, 2, 3, 4],
         [5, 6, 7, 8],
         [9, 10, 11, 12],
         [13, 14, 15, 16]])
