from flask import Flask, session, g
import config
from exts import db, mail, cache
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate
from sqlalchemy import text


app = Flask(__name__)
# bonding with configuration file
app.config.from_object(config)

db.init_app(app)  # 如果没有extension，则是 db = SQLAlchemy(app), 但这样在程序分开封装后会导致循环引用问题。
# 现在就是，先创建，再和程序绑定


with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())
# It's used for verify if the app is connected


migrate = Migrate(app, db)

# flask db init：
# flask db migrate：
# flask db upgrade：


############### Email Service #################
mail.init_app(app)

############## Cache Service #############
cache.init_app(app)


# blueprints is used for modularization

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# before_request / before_first_request/ after_request   （hook function）
@app.before_request
def my_before_request():
    user_id = session.get("user_id")  # flask 可以帮我们做好解密
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)   # g = global variable
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}
# Define application context process to simplify your code

if __name__ == '__main__':
    app.run()
