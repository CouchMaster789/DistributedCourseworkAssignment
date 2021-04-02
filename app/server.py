import asyncio
import logging
import sys

import grpc
import numpy as np

import matrix_computations_pb2
import matrix_computations_pb2_grpc
from app.utils import decode_matrix, encode_matrix


class Computer(matrix_computations_pb2_grpc.ComputerServicer):
    def multiply_block(self, request, context: grpc.aio.ServicerContext):
        result = np.matmul(decode_matrix(request.matrix_1), decode_matrix(request.matrix_2))

        return matrix_computations_pb2.ComputationResult(matrix=encode_matrix(result))

    def add_block(self, request, context: grpc.aio.ServicerContext):
        result = np.add(decode_matrix(request.matrix_1), decode_matrix(request.matrix_2))

        return matrix_computations_pb2.ComputationResult(matrix=encode_matrix(result))


async def serve(port) -> None:
    server = grpc.aio.server()
    matrix_computations_pb2_grpc.add_ComputerServicer_to_server(Computer(), server)
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)


def serve_runner(port=50052):
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve(port))


if __name__ == '__main__':
    serve_runner(int(sys.argv[1]))
