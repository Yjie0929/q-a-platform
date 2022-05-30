from exts import db
from datetime import datetime  # 获取当前时间


class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)  # 保存当前时间


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)  # 密码字符长度要设置200+因为加密后的长度会很长
    join_time = db.Column(db.DateTime, default=datetime.now)


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='questions')
    # 模板层连接至User表：QuestionModel对象.author
    # 模板层读取User表的详细数据：QuestionModel对象.author.username，通过外键，访问User表的username对象


class AnswerModel(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.relationship('QuestionModel', backref=db.backref('answers', order_by=create_time.desc()))
    author = db.relationship('User', backref='answers')
