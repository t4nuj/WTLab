from flask import jsonify, request, session, redirect, abort
from pinboard_app import app, db, card_schema, cards_schema
from pinboard_app.models import User, List, Card
from decorators import logged_in


@app.route('/api/card/', methods=['GET'])
@logged_in
def get_cards():
    try:
        list_id = request.args['list']
        list = List.query.get_or_404(list_id)

        if session['user_id'] not in [user.id for user in list.board.users]:
            return abort(403)

        cards = [card for card in list.cards]
        card_json = cards_schema.dump(cards)
        return jsonify({'cards': card_json.data})

    except KeyError:
        return jsonify({'Error': 'Incorect form of request'}), 400


@app.route('/api/card/', methods=['POST'])
@logged_in
def post_card():
    try:
        data = request.get_json()

        if data is None:
            return jsonify({'Error': 'Incorect form of request'}), 400

        list = List.query.get_or_404(data['list'])

        if session['user_id'] not in [user.id for user in list.board.users]:
            return abort(403)

        title, content = data['title'], ''

        try:
            content = data['content']
        except KeyError:
            content = ''

        card = Card(title=title, content=content)

        list.cards.append(card)
        db.session.add(card)
        card_json = card_schema.dump(card)
        return jsonify(card_json.data)

    except KeyError:
        return jsonify({'Error': 'Incorect form of request'}), 400


@app.route('/api/card/<int:id>/', methods=['GET'])
@logged_in
def get_card(id):
    card = Card.query.get_or_404(id)

    if session['user_id'] not in [user.id for user in card.list.board.users]:
        return abort(403)

    print card.id, card.title
    card_json = card_schema.dump(card)
    print card_json.data
    return jsonify(card_json.data)


@app.route('/api/card/<int:id>/', methods=['PUT'])
@logged_in
def put_card(id):
    card = Card.query.get_or_404(id)

    if session['user_id'] not in [user.id for user in card.list.board.users]:
        abort(403)

    data = request.get_json()
    data.pop('id', None)
    db.session.query(List).filter_by(id=id).update(data)
    return jsonify(data)
