from flask import Blueprint, jsonify, render_template, request

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
    matrix_result = [[0 for _ in range(len(row))] for row in matrix_1]

    for i in range(len(matrix_1)):
        for j in range(len(matrix_2[0])):
            for k in range(len(matrix_2)):
                matrix_result[i][j] += matrix_1[i][k] * matrix_2[k][j]

    return jsonify({"result": ";".join([",".join([str(item) for item in row]) for row in matrix_result])}), 200
