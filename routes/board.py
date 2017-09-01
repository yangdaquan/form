from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/admin")
def index():
    u = current_user()
    bs = Board.find_all()
    return render_template('board/admin_index.html',user=u,bs=bs)
    ...


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    Board.new(form)
    return redirect(url_for('topic.index'))

