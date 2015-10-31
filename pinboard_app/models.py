from flask.ext.sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

user_boards = db.Table('user_boards',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('board_id',
                                 db.Integer, db.ForeignKey('board.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(200))


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lists = db.relationship('List', backref='board', lazy='dynamic')
    users = db.relationship('User', secondary=user_boards, backref='boards')


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    cards = db.relationship('Card', backref='list', lazy='dynamic')


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.String(100))
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))


class BoardSchema(ma.ModelSchema):

    class Meta:
        model = Board


class ListSchema(ma.ModelSchema):

    class Meta:
        model = List


class CardSchema(ma.ModelSchema):

    class Meta:
        model = Card


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
