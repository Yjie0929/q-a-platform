from flask import Flask, session, g
import config
from exts import db, mail
from blueprints import qa_bp
from blueprints import user_bp
from flask_migrate import Migrate
from models import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)
migrate = Migrate(app, db)


@app.before_request  # 在请求之前执行
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = User.query.get(user_id)
            g.user = user  # 将user命名为'user'，并绑定至g，将user变为全局变量：g
        except:
            g.user = None


# 请求来了 -> before-request -> 执行视图函数 -> 返回视图函数中的模板 -> context_processor

@app.context_processor  # 上下文处理器，执行后渲染的任何模板都会执行该视图函数
def context_processor():
    if hasattr(g, 'user'):  # 如果user有了则执行
        return {'user': g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
