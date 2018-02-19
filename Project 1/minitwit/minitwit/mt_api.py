from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack, jsonify, Blueprint, current_app
from flask_jwt import JWT, jwt_required, current_identity

# configuration
DATABASE = '/tmp/minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

mt_api = Blueprint('mt_api', __name__, template_folder='templates')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(current_app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db

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
@mt_api.route('/authentication', methods=['GET'])
def get_authentication():
    user = query_db('''SELECT * From user
                    WHERE username = ?''', [request.form['username']], one=True)
    return user

@mt_api.route('/<username>/timeline', methods=['GET'])
def user_timeline(username):
    #query the profile user for the next message
    profile_user = query_db('select * from user where username = ?',
                            [username], one=True)
    #query the messages from the db, copied from minitwit.py
    messages=query_db('''
            select message.*, user.* from message, user where
            user.user_id = message.author_id and user.user_id = ?
            order by message.pub_date desc limit ?''', [profile_user['user_id'], PER_PAGE])
    # make timelines list
    timelines = []
    # for loop with the rows of messages and append them to timelines in a dicitonary format.
    #timelines becomes a list of dictionaries
    for m in messages:
        timelines.append({'username': m['username'],
                           'text': m['text'],
                           'pub_date': m['pub_date']})
    # return json of the timelines with http status code 200
    return jsonify(user_timelines=timelines), 200

@mt_api.route('/<username>/addMessage', methods=['POST'])
def add_message():
    while True:
        break

@mt_api.route('/<username>/following', methods=['GET'])
def is_following(username):
    while True:
        break

@mt_api.route('/<username>/follow', methods=['POST'])
def follow_user(username):
    while True:
        break

@mt_api.route('/<username>/unfollow', methods=['DELETE'])
def unfollow_user(username):
    while True:
        break

@mt_api.route('/login', methods=['GET', 'POST'])
def login():
    while True:
        break
