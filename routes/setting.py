from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from models.user import User
from models.topic import Topic
from models.board import Board
import os
import uuid

from routes import current_user
from utils import log

main = Blueprint('setting', __name__)


@main.route("/")
def index():
    u = current_user()
    return render_template("setting.html", user=u)


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


@main.route('/image/add', methods=["POST"])
def add_img():
    u = current_user()
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]

    if valid_suffix(suffix):
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('user_image', filename))
        u.user_image = '/uploads/' + filename
        print('u.user_image',u.user_image)
        u.save()

    return redirect(url_for(".index"))


# send_from_directory
# nginx 静态文件
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory('user_image', filename)


@main.route("/signature/update", methods=['POST'])
def signature():
    form = request.form
    u = current_user()
    u.signature = form.get('signature', '')
    u.save()
    return redirect(url_for('.index'))


@main.route("/password/update", methods=['POST'])
def password():
    form = request.form
    u = current_user()
    old_pass = form.get('old_pass', '')
    new_pass = form.get('new_pass', '')

    if u.salted_password(old_pass) == u.password and len(new_pass) > 2:
        u.password = u.salted_password(new_pass)
        u.save()
        return redirect(url_for('.index'))
    else:
        return redirect(url_for('.index'))
