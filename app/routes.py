from asgiref.sync import async_to_sync
from flask import Blueprint, jsonify, render_template, request

from app.client import run

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html"), 200


@bp.route("/multiply", methods=["POST"])
def multiply():
    matrix_1 = request.form.get("matrix_1", "", str)
    matrix_2 = request.form.get("matrix_2", "", str)

    if not (matrix_1 or matrix_2):
        return jsonify({"msg": "At least one matrix is missing, two matrices are required for multiplication."}), 400

    matrix_1 = [[int(item) for item in row.split(",")] for row in matrix_1.split(";")]
    matrix_2 = [[int(item) for item in row.split(",")] for row in matrix_2.split(";")]

    matrix_result = async_to_sync(run)(matrix_1, matrix_2, deadline=0.1)

    return jsonify({"result": ";".join([",".join([str(item) for item in row]) for row in matrix_result])}), 200
