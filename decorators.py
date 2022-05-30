from flask import g, redirect, url_for
from functools import wraps


def login_required(func):  # 登陆以后执行
    @wraps(func)  # 被装饰的函数实际上已经是另一个函数了，这种情况下可能会导致函数名、属性发生改变，所以该操作是为了防止属性丢失
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))

    return wrapper
