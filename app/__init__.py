import logging
from multiprocessing.context import Process

from flask import Flask

from app.server import serve_runner

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.addHandler(console_handler)


def create_app():
    app = Flask(__name__)

    logger.info("Server starting...")

    from app.routes import bp
    app.register_blueprint(bp)

    starting_port = 50052
    for port in range(starting_port, starting_port + 8):
        process = Process(target=serve_runner, args=(port,))
        process.start()

    return app
