HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_project'
USERNAME = 'root'
PASSWORD = 'Lyl1030'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'adasfzfd1edad21w'

MAIL_SERVER = 'smtp.qq.com'  # 服务器地址，选择qq邮箱
MAIL_PORT = 465  # 固定写法
MAIL_USE_TLS = False  # 固定写法
MAIL_USE_SSL = True  # 固定写法
MAIL_DEBUG = True  # 投入使用要变为False
MAIL_USERNAME = '634054241@qq.com'  # 我本人的邮箱
MAIL_PASSWORD = 'cncoxandipvybehb'  # 我本人邮箱的POP3/SMTP授权码
MAIL_DEFAULT_SENDER = '634054241@qq.com'
# MAIL_MAX_EMAILS  # 不需要设置
# MAIL_SUPPRESS_SEND  # 不需要设置
# MAIL_ASCII_ATTACHMENTS  # 不需要设置
