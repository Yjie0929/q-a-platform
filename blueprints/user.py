from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash
)
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, User
import string
import random
from datetime import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash  # 用于MD5加密、MD5是否一致验证

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def login() -> ...:
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):  # 判断用户是否存在、数据库中的密码是否与输入的一致（MD5检测）
                session['user_id'] = user.id  # 使用session，记住该用户id的登陆状态
                return redirect('/')
            else:
                flash('邮箱与密码不匹配')  # 设置错误提醒，需要在模板层设置
                return redirect(url_for('user.login'))
        else:
            flash('邮箱与密码格式错误！')
            return redirect(url_for('user.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)  # 存储前端通过form表单上传的数据
        if form.validate():  # 判断是否验证通过
            email = form.email.data  # 获取前端form表单中email数据，并调用form表单验证
            username = form.username.data  # 获取前端form表单中username数据，并调用form表单验证
            password = form.password.data  # 获取前端form表单中password数据，并调用form表单验证
            hash_password = generate_password_hash(password)  # MD5加密
            user = User(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))  # 登陆完成后，视图重定向至登陆页面
        else:
            return redirect(url_for('user.register'))


@bp.route('/captcha', methods=['POST'])
def get_captcha():
    email = request.args.get('email')  # 抓取查询字符串email
    code_string = string.ascii_letters + string.digits
    captcha = ''.join(random.sample(code_string, 4))
    if email:
        message = Message(
            subject='邮箱测试',  # 邮件主题设置
            recipients=[email],  # 收件人指定
            body=f'验证码是{captcha}',  # 邮件内容
            sender='634054241@qq.com',  # 发送者设置
        )
        mail.send(message)  # 发送邮件
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()  # 获取数据库的第一条数据
        if captcha_model:
            captcha_model.captcha = captcha  # 数据更新，把老的captcha更新为新的captcha
            captcha_model.create_time = datetime.now()  # 获取当前时间，写入数据库
            db.session.commit()  # 执行修改
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        return jsonify({'code': 200})  # 返回给register.js文件的success function (res)回调函数，返回200表示成功
    else:
        # 返回给register.js文件的success function (res)回调函数，返回400表示失败
        return jsonify({'code': 200, 'message': '请先传递邮箱'})


@bp.route('/logout', methods=['GET'])
def logout() -> ...:
    session.clear()
    return redirect(url_for('user.login'))
