from flask import jsonify, request, session, abort
from pinboard_app import app, db, board_schema, boards_schema, user_schema
from pinboard_app.models import Board, User
from decorators import logged_in


@app.teardown_request
def teardown_request(exception):
    if exception is None:
        db.session.commit()


@app.route('/board/', methods=['GET'])
@logged_in
def get_boards():
    user = User.query.get(session['user_id'])
    boards = [board for board in user.boards]
    boards_json = boards_schema.dump(boards)
    return jsonify({"boards": boards_json.data})


@app.route('/board/', methods=['POST'])
@logged_in
def post_board():
    data = request.get_json()
    if data is None:
        return jsonify({'Error': "Incorrect form of Data"}), 400
    try:
        board = Board(name=data['name'], users=[session['user_id']])
        db.session.add(board)
    except KeyError:
        return jsonify({'Error': "Incorrect form of Data"}), 400


@app.route('/board/<int:id>/', methods=['GET'])
@logged_in
def get_board(id):
    board = Board.query.get_or_404(id)

    if session['user_id'] not in \
            [board.id for board in User.query.get(session['user_id']).boards]:
        abort(403)

    board_result = board_schema.dump(board)
    return jsonify(board_result.data)


@app.route('/board/<int:id>/', methods=['PUT'])
@logged_in
def put_board(id):
    if id in [board.id for board in User.query.get(session['user_id']).boards]:
        data = request.get_json()
        data.pop('id', None)
        db.session.query(Board).filter_by(id=id).update(data)
        return jsonify(data)
    else:
        abort(403)
