# /home/tanuj/Work/wt/original/pinboard/venv/bin/pyhton
from flask import Flask, jsonify, request, session, redirect
from models import db, ma, Board, List, Card, BoardSchema, ListSchema, CardSchema, UserSchema
from flask_marshmallow import Marshmallow
# from sqlalchemy.ext.declarative import DeclarativeMeta
# from mongokit import Connection, Document
import json

import datetime
app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
ma.init_app(app)

# connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])


board_schema = BoardSchema()
boards_schema = BoardSchema(many=True, only=('id', 'name'))
list_schema = ListSchema()
lists_schema = ListSchema(many=True)
card_schema = CardSchema()
cards_schema = CardSchema(many=True)
user_schema = UserSchema()

from pinboard_app.views import board,list,card,auth

app.secret_key = '>TJ\x88)X-F\x86\x04\x00\x8ff\xcb\x1c\xc5\x85R.\x9b.|\xdb\x97\xdb:\xa1\xd3E\x8a\xb4)\xd8\xa0\xa7G\xbb\x81\x0b-\xd1\x81\\\xd4\xd3\x0f`y\x82g'

# if __name__ == '__main__':
#     # create_dummy_data()
#     app.run(debug=True)
