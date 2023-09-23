from flask import Blueprint, request, render_template, redirect, url_for, g
from .forms import QuestionForm
from exts import db
from models import QuestionModel
from decorators import login_required

# /auth
bp = Blueprint("qa", __name__)  #不加prefix为了能访问首页， 如果要加就加默认值 /

# http://127.0.0.1:5000
@bp.route("/")
def index():
    return render_template("index.html")

# @bp.route("/base")

@bp.route("/qa/publicize", methods = ['GET', 'POST'])
@login_required
def public_question():
    # # 简易版 => 后面wrap成一个decorator
    # if not g.user:
    #     return redirect(url_for("auth.login"))
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title = title, content = content, author = g.user)
            db.session.add(question)
            db.session.commit()
            # todo: 跳转到这篇问答的详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))