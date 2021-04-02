from multiprocessing.context import Process

from flask import Flask

from app.server import serve_runner


def create_app():
    app = Flask(__name__)

    from app.routes import bp
    app.register_blueprint(bp)

    starting_port = 50052
    for port in range(starting_port, starting_port + 8):
        process = Process(target=serve_runner, args=(port,))
        process.start()

    return app
