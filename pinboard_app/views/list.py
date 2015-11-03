from flask import jsonify, request, session, redirect, abort
from pinboard_app import app, db, list_schema, lists_schema
from pinboard_app.models import User, Board, List
from decorators import logged_in


@app.route('/api/list/', methods=['GET'])
@logged_in
def get_lists():
    try:
        board_id = request.args['board']
        board = Board.query.get_or_404(board_id)

        if session['user_id'] not in [user.id for user in board.users]:
            return abort(403)

        lists = [list for list in board.lists]
        list_json = lists_schema.dump(lists)
        return jsonify({'lists': list_json.data})

    except KeyError:
        return jsonify({'Error': 'Incorect form of request'}), 400


@app.route('/api/list/', methods=['POST'])
@logged_in
def post_list():
    try:
        data = request.get_json()

        if data is None:
            return jsonify({'Error': 'Incorect form of request'}), 400

        board = Board.query.get_or_404(data['board'])

        if session['user_id'] not in [user.id for user in board.users]:
            return abort(403)

        list = List(title=data['title'])
        board.lists.append(list)
        db.session.add(list)
        list_json = list_schema.dump(list)
        return jsonify(list_json.data)

    except KeyError:
        return jsonify({'Error': 'Incorect form of request'}), 400


@app.route('/api/list/<int:id>/', methods=['GET'])
@logged_in
def get_list(id):
    list = List.query.get_or_404(id)

    if session['user_id'] not in [user.id for user in list.board.users]:
        return abort(403)

    list_json = list_schema.dump(list)
    return jsonify(list_json.data)


@app.route('/api/list/<int:id>/', methods=['PUT'])
@logged_in
def put_list(id):
    list = List.query.get_or_404(id)

    if session['user_id'] not in [user.id for user in list.board.users]:
        abort(403)

    data = request.get_json()
    data.pop('id', None)
    db.session.query(List).filter_by(id=id).update(data)
    return jsonify(data)
