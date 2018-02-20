from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack, jsonify, Blueprint, current_app
from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_simple import jwt_required, get_jwt_identity, create_jwt

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
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "Unauthorized"}), 401
    #ID = get_user_id(profile_user)
    #query the messages from the db, copied from minitwit.py
    messages=query_db('''
            select message.*, user.* from message, user where
            user.user_id = message.author_id and user.user_id = ?
            order by message.pub_date desc limit ?''',
            [userID, PER_PAGE])
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
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "Unauthorized"}), 401


@mt_api.route('/<username>/following', methods=['GET'])
def following(username):
    #query the profile user for the next message
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "Unauthorized"}), 401

    people_following = query_db('''
                                select * from follower where
                                follower.whom_id = ?''',
                                [userID])
    people = []
    for p in people_following:
        person = query_db('''select * from user where user_id = ?''',
                            [p['whom_id']])
        people.append({'followers': str(person)})
    return jsonify(followers=people), 200

@mt_api.route('/<username>/followers', methods=['GET'])
def followers(username):
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "Unauthorized"}), 401
    people_following = query_db('''
                                select * from follower where
                                follower.whom_id = ?''', [userID])
    people = []
    for p in people_following:
        person = query_db('''select * from user where user_id = ?''',
                            [p['whom_id']])
        people.append({'followers': str(person)})
    return jsonify(followers=people), 200
@mt_api.route('/<username>/follow', methods=['POST'])
def follow_user(username):
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "Unauthorized"}), 401

@mt_api.route('/<username>/unfollow', methods=['DELETE'])
def unfollow_user(username):
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "Unauthorized"}), 401
