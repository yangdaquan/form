from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from models.reply import Reply
from routes import *

from models.topic import Topic
from models.board import Board
import uuid

main = Blueprint('user', __name__)


@main.route('/<string:username>')
def detail(username):
    user = User.find_by(username=username)
    ts = Topic.topic_sort(user.id)
    rs = Reply.topic_of_reply_sort(user.id)
    u = current_user()
    if u is not None:
        return render_template("user/homepage.html", user=u, ts=ts, rs=rs)
