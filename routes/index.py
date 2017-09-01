from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)

from models.board import Board
from models.topic import Topic
from models.user import User
from routes import current_user

from utils import log

main = Blueprint('index', __name__)



"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""

@main.route("/")
def visit():
    u = current_user()
    if u is not None:
        session.pop('user_id')
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    bs = Board.all()

    return render_template("visit.html", ms=ms, bs=bs, bid=board_id)


@main.route("/login_and_register")
def login_and_register():
    return render_template("login_and_register.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('index.login_and_register'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('index.login_and_register'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))

@main.route('/search')
def search():
    value = request.args.get('key')
    url =  'https://www.baidu.com/s?wd={}'.format(value)
    return redirect(url)



