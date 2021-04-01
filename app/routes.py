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

    print("matrix 1:", matrix_1)
    print("matrix 2:", matrix_2)

    return jsonify({"result": matrix_1}), 200
