
from functools import wraps
from flask import g, redirect, url_for


def login_required(func):
    # 保留function的信息
    @wraps(func)
    # func(a,b,c)
    # func(1, 2, c = 3)
    def inner(*args, **kwargs):  # 这个函数名字可以随便取
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))
    return inner