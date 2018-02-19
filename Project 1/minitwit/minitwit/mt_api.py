from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack, jsonify
from flask_jwt import JWT, jwt_required, current_identity

# configuration
DATABASE = '/tmp/minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

app = Flask('mt_api')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db

@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

# HTTP service GET
@app.route('/login', methods=['GET'])
def get_authentication():
    user = query_db('''SELECT * From user
                    WHERE username = ?''', [request.form['username']], one=True)
    return user

@app.route('/<username>/timeline', methods=['GET'])
def user_timeline():
    while True:
        break

@app.route('/<username>/addMessage', methods=['POST'])
def add_message():
    while True:
        break

@app.route('/<username>/following', methods=['GET'])
def is_following(username):
    while True:
        break

@app.route('/<username>/follow', methods=['POST'])
def follow_user(username):
    while True:
        break

@app.route('/<username>/follow', methods=['DELETE'])
def unfollow_user(username):
    while True:
        break

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = query_db('''SELECT * FROM users
                        WHERE username=?''', [request.form['username']], one=True)
        d= dict(user)
        return jsonify(d)
