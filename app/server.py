import logging
from concurrent import futures

import grpc
import numpy as np

import matrix_computations_pb2
import matrix_computations_pb2_grpc
from utils import decode_matrix, encode_matrix


class Computer(matrix_computations_pb2_grpc.ComputerServicer):
    def multiply_block(self, request, context):
        result = np.matmul(decode_matrix(request.matrix_1), decode_matrix(request.matrix_2))

        return matrix_computations_pb2.ComputationResult(matrix=encode_matrix(result))

    def add_block(self, request, context):
        result = np.add(decode_matrix(request.matrix_1), decode_matrix(request.matrix_2))

        return matrix_computations_pb2.ComputationResult(matrix=encode_matrix(result))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matrix_computations_pb2_grpc.add_ComputerServicer_to_server(Computer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
