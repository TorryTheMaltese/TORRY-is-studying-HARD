from flask_login import UserMixin
from app import login, db
from sqlalchemy.sql import func
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    __tablename__ = "tbl_user"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), index=True, unique=True)
    user_pw = db.Column(db.String(94))
    user_name = db.Column(db.String(64))
    user_registration_date = db.Column(db.DATETIME, default=func.now())
    user_last_sign_in = db.Column(db.DATETIME, default=datetime.utcnow())

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('id')
        self.user_email = kwargs.get('user_email')
        self.user_pw = generate_password_hash(kwargs.get('user_pw'))
        self.user_name = kwargs.get('user_name')

    def __repr__(self):
        return '<USER {}>'.format(self.user_email)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}

    def set_user_pw(self, password):
        self.user_pw = generate_password_hash(password)

    def check_user_pw(self, password):
        return check_password_hash(self.user_pw, password)

    def avatar(self, size):
        digest = md5(self.user_email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{0}?d=identicon&s={1}'.format(digest, size)
