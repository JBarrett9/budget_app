from flask import current_app
from datetime import date
from budgetapp import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    content_id = db.Column(db.Integer)
    bills = db.relationship('Bill', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_add_token(self, expires_sec=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'content_id': self.content_id}).decode('utf-8')

    @staticmethod
    def verify_add_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            content_id = s.loads(token)['content_id']
        except:
            return None
        return User.query.get(content_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fixed_amt = db.Column(db.Boolean)
    due = db.Column(db.DateTime, nullable=False)
    recurring = db.Column(db.Boolean)
    frequency = db.Column(db.String)
    category = db.Column(db.String)
    url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.content_id'))

    def __repr__(self):
        return f"{self.name} ${self.amount} due: {self.due.strftime('%m/%d')}"


class PastBills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fixed_amt = db.Column(db.Boolean)
    due = db.Column(db.DateTime, nullable=False)
    recurring = db.Column(db.Boolean)
    frequency = db.Column(db.String)
    category = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.content_id'))

    def __repr__(self):
        return f"{self.name} ${self.amount} due: {self.due.strftime('%m/%d')}"
