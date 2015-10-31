from pinboard_app import app,db
from pinboard_app.models import User,Board,Card,List,user_boards
from datetime import datetime

with app.app_context():
    db.drop_all()
    db.create_all()
    user1 = User()
    user1.username = 'tanuj'
    user1.password = 'admin'
    card1 = Card(title='Mera Card 1')
    card2 = Card(title='Mera Card 2')
    card3 = Card(title='Mera Card 3')
    list1 = List(title='Meri List 1', cards=[card1])
    list2 = List(title='Meri List 2', cards=[card2])
    list3 = List(title='Meri List 3', cards=[card3])
    board = Board(name='Mera Board 2', lists=[list1, list2, list3])
    board.users.append(user1)
    db.session.add(card1)
    db.session.add(card2)
    db.session.add(card3)
    db.session.add(list1)
    db.session.add(list2)
    db.session.add(board)
    db.session.add(list3)
    db.session.commit()
