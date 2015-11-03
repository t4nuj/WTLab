from flask import render_template, url_for, request, session, redirect ,\
    send_from_directory
from pinboard_app import app, db, user_schema
from pinboard_app.models import User
from decorators import logged_in


@app.route('/', methods=['GET'])
def index():
    try:
        if not session['logged_in']:
            return render_template('html/login.html')
        else:
            return redirect(url_for('show_user',
                                    username=session['username']))
    except KeyError:
        session['logged_in'] = False
        return render_template('html/login.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        try:
            if session['logged_in']:
                return redirect(url_for('show_user',
                                        username=session['username']))
            else:
                return render_template('html/register.html')
        except KeyError:
            return render_template('html/register.html')
    else:
        error = None
        username = request.form['username']
        password = request.form['password']
        unique = User.query.filter_by(username=username).first()
        # print unique.username
        if unique is None:
            if password is not None:
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user.id
                return redirect(url_for('show_user', username=username))
            else:
                error = 'Empty password not allowed.'
        else:
            error = 'Username already exists.'

        return render_template('html/register.html', error=error)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = 'Incorrect username'
        elif password != user.password:
            error = 'Incorrect password'
        else:
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user.id
            print username
            return redirect(url_for('show_user', username=username))
    return render_template('html/login.html', error=error)


@app.route('/logout/', methods=["GET"])
@logged_in
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/<username>/')
@logged_in
def show_user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('html/showuser.html', user=user)
