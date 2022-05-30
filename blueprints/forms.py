import wtforms
from wtforms.validators import length, email, EqualTo, input_required
from models import EmailCaptchaModel, User


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=3, max=20)])


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    password = wtforms.StringField(validators=[length(min=3, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    def validate_captcha(self, field) -> ...:  # 在captcha在被验证时，该方法会自动执行，取决于_后面的单词对应
        captcha = field.data  # 获取captcha的值，取到什么值取决于_后面跟的对象
        captcha_model = EmailCaptchaModel.query.filter_by(email=self.email.data).first()
        # 对数据库中email字段为一级验证的email的值定位
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError('邮箱验证码错误')

    def validate_email(self, field):
        user_model = User.query.filter_by(email=self.email.data).first()
        if user_model:
            raise wtforms.ValidationError('邮箱已存在')


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=5)])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=5)])
