import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel


# Form: 主要用于验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):   # 这个类继承自 wtforms 下面的一个类 Form
    # 前端会传过来 email
    email = wtforms.StringField(validators = [Email(message = "email format is not valid")])
    # validators 里的email 验证这个邮箱是不是一个正确的邮箱格式
    captcha = wtforms.StringField(validators = [Length(min = 4, max = 4, message = "auth code format is not valid")])
    username = wtforms.StringField(validators = [Length(min = 3, max = 20, message = "username format is not valid")])
    password = wtforms.StringField(validators = [Length(min = 6, max = 20, message = "password format is not valid")])
    password_confirm = wtforms.StringField(validators = [EqualTo("password", message = "Two passwords do not match.")])

    # 自定义验证
    # 1. 邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:   # 非空对象的真值（true value）是 true， 空对象的真值是 false
            raise wtforms.ValidationError(message = "This email has been registered!")

    # 2. 验证码是否正确
    def validate_captcha(self, field):  # field 是一个 StringField对象 （wtform 中的field类）
        captcha = field.data  # data 是 字段对象的属性
        email = self.email.data  # 相当于java里的this
        captcha_model: EmailCaptchaModel.query.filter(email = email, captcha = captcha).first()
        if not captcha:
            raise wtforms.ValidationError(message = "Email or Auth Code is not correct!")
        # todo: 可以删掉 captcha_model, 也可以定期清理
        # 这里比较推荐定期清理
        # 因为影响一个网站性能最大的就是sql语句操作的频繁程度
        # 所以我们这里还是尽量少开 db.session

    # Note！！！！
    # WTForms 会查找并调用你在表单类中为特定字段定义的自定义验证方法。这些方法的名字必须以 validate_ 开头，后面跟着字段的名字。

class LoginForm(wtforms.Form):
    # 前端会传过来 email & password
    email = wtforms.StringField(validators = [Email(message = "email format is not valid")])
    password = wtforms.StringField(validators = [Length(min = 6, max = 20, message = "password format is not valid")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="Title Format Error!")])
    content = wtforms.StringField(validators=[Length(min=3,message="Content Format Error")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="Content Format Error")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="Answer must be associated with question!")])
