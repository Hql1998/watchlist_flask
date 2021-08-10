from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, sys
from flask_login import LoginManager

app = Flask(__name__)

print(app.root_path)
print()
Win = sys.platform.startswith("win")
if Win:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(os.path.dirname(app.root_path), "data.db")
app.config["SECRET_KEY"] = "dev"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(user_id)
    return user

@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

from watchlist import views, errors, commands