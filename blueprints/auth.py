import random

from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask import request
from flask_mail import Message
from exts import db, mail, cache
import string
from models import EmailCaptchaModel, UserModel  # 不加 . 表示从顶级包中import
from .forms import RegisterForm, LoginForm  # 加 . 表示从当前包中 import
from werkzeug.security import generate_password_hash, check_password_hash


# /auth
bp = Blueprint("auth", __name__, url_prefix = "/auth")

# 如果route没有指定method，默认就是get
@bp.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email = email).first()
            # 登录失败，就会回到login页面重新登录
            if not user:
                print("Email has not been registered")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # cookie：
                # cookie中不适合存储太多的数据，只适合存储少量的数据
                # cookie一般用来存放登录授权的东西
                # flask中的session，是经过加密后存储在cookie中的
                session['user_id'] = user.id
                # session 是一种服务器的解决方案
                return redirect("/")  # 登录成功后跳转到首页
            else:
                print("Email or Password is not correct!")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


# GET: 从服务器获取数据
# POST: 将客户端的数据提交给服务器
@bp.route("/register", methods=['GET','POST'])
def register():
    # While Click sign-up button, we need to fetch the form
    if request.method == 'GET':
        return render_template("register.html")
    # Then, 我们还需要验证用户的验证码是否和我们发送的验证码一致
    # 表单验证：flask-wtf (wtforms)
    else:
        form = RegisterForm(request.form)  # request.form -- 拿到用户提交上来的数据
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email = email, username = username, password = generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
            # url_for()用于动态地生成应用中特定视图函数的 URL。
            # 用于指向应用中的路由的
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route("/captcha/email")
def send_mail_captcha():
    # /captcha/email/<email address>
    # /captcha/email?email=xxx@gmail.com
    email = request.args.get("email")
    auth_code = get_captcha()
    # I/O operation.
    # I/O 操作（输入/输出操作）通常指的是与系统外部交互的操作，
    # 包括读取和写入文件、网络请求、数据库查询等。
    # 当你的程序向外部发送数据（例如通过网络发送电子邮件），或者从外部获取数据（例如读取一个文件或接收网络请求）时，这都是 I/O 操作。
    # I/O 操作一般都比较耗时，所以我们可以用任务队列去处理它
    message = Message(subject = "Quest Auth Code",
                      recipients = [email],
                      body = f"Your Quest Auth Code: {auth_code}")
    mail.send(message)
    # 按道理应该存在缓存，因为这个验证码很快就没有用了，eg. memcached/redis(比较强大且有同步机制)
    # 用数据库方式存储
    email_captcha_record = EmailCaptchaModel(email = email, captcha = auth_code)
    db.session.add(email_captcha_record)
    db.session.commit()

    # 存在缓存
    # cache.set(email, auth_code, timeout = 300)

    # return "Auth Code has been sent to your email"
    # RESTful API
    # {code: 200/400/500, message: "", data: {}}
    return jsonify({"code": 200, "message": "", "data": None})

def get_captcha():
    # 4/6: 随机数组、字母和数字组合
    source = string.digits * 4  # 0123456789012345678901234567890123456789 => 从中选四位
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)  # 将captcha这个列表中所有元素连接成一个字符串， “”表示所有元素只见没有任何字符
    return captcha
# 这里是伪随机，实际上安全性并不是特别高



@bp.route("/mail/test")
def mail_test():
    message = Message(subject = "email test", recipients = ["myin08@syr.edu"], body = "test for flask email")
    mail.send(message)
    return "邮件发送成功!"

@bp.route('/logout')
def logout():
    session.clear() # 删掉所有的session信息
    return redirect("/")

