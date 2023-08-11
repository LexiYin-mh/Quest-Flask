
# exts.py：这个文件存在的意义就是为了解决循环引用的问题
# short for extension

# flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache

db = SQLAlchemy()

"""
如果没有这行代码
在 app.py --- 我们会有 from models import UserModel
在models.py --- from app import db --> UserModel(db.Model)
"""

mail = Mail()

cache = Cache()

