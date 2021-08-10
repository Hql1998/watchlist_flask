from watchlist import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# create table classes
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    pwd_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.pwd_hash, password)


class Novel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))