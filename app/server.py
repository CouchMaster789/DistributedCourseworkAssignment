import asyncio
import logging
import sys
import time

import grpc
import numpy as np

import matrix_computations_pb2
import matrix_computations_pb2_grpc
from app.utils import decode_matrix, encode_matrix, GRPC_OPTIONS

logger = logging.getLogger("main")


class Computer(matrix_computations_pb2_grpc.ComputerServicer):
    port_id = None

    def __init__(self, *args, port_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.port_id = port_id

    def multiply_block(self, request, context: grpc.aio.ServicerContext):
        start = time.time()
        logger.info(f"port {self.port_id} is running a multiplication operation...")

        result = np.matmul(decode_matrix(request.matrix_1), decode_matrix(request.matrix_2))

        logger.info(
            f"port {self.port_id} has completed a multiplication operation in {time.time() - start:.03} seconds!")

        return matrix_computations_pb2.ComputationResult(matrix=encode_matrix(result))

    def add_block(self, request, context: grpc.aio.ServicerContext):
        start = time.time()
        logger.info(f"port {self.port_id} is running an addition operation...")

        result = np.add(decode_matrix(request.matrix_1), decode_matrix(request.matrix_2))

        logger.info(f"port {self.port_id} has completed an addition operation in {time.time() - start:.03} seconds!")

        return matrix_computations_pb2.ComputationResult(matrix=encode_matrix(result))


async def serve(port) -> None:
    server = grpc.aio.server(options=GRPC_OPTIONS)
    matrix_computations_pb2_grpc.add_ComputerServicer_to_server(Computer(port_id=port), server)
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting server on {listen_addr}. This server will be known by its port.", )
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)


def serve_runner(port=50052):
    asyncio.run(serve(port))


if __name__ == '__main__':
    serve_runner(int(sys.argv[1]))
