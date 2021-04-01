from flask import Blueprint, jsonify, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html"), 200
