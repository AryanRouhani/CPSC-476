import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack, jsonify, Blueprint, current_app
from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_simple import jwt_required, get_jwt_identity, create_jwt
from werkzeug import check_password_hash, generate_password_hash

# configuration
DATABASE = '/tmp/minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

# mt_api = Blueprint('mt_api', __name__, template_folder='templates')

# create our little application :)
mt_api = Flask('mt_api')
mt_api.config.from_object(__name__)
mt_api.config.from_envvar('MINITWIT_SETTINGS', silent=True)
# mt_api.register_blueprint(mt_api)

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

@mt_api.route('/hello', methods=['GET'])
def hooman():
    return "hello hooman!"

# HTTP service GET
@mt_api.route('/internal/authentication', methods=['GET'])
def authentication():
    username = 'shirley'
    password = '12345'
    user = query_db(''' SELECT username FROM user''')
    passwords = query_db(''' SELECT pw_hash FROM user''')

    for i in range(len(passwords)):
        print str(passwords[i][0])
        if password in str(passwords[i][0]) and username in str(user[i][0]):
            #print user[i]
            return jsonify({'Message': 'Username and Password is verified'})

    return jsonify({'Message':'Username and Password not verified'})

@mt_api.route('/<username>', methods=['GET'])
def timeline(username):
    """Shows a users timeline or if no user is logged in it will
    redirect to the public timeline.  This timeline shows the user's
    messages as well as all the messages of followed users.
    """
    userID = get_user_id(username)

    if userID == None:
        return jsonify({'Message': 'No such user'}), 404
        
    messages=query_db('''
            select message.*, user.* from message, user where
            user.user_id = message.author_id and user.user_id = ?
            order by message.pub_date desc limit ?''',
            [userID, PER_PAGE])
        #make timeline list 
        
    timelines = [] 
    for m in messages:
            timelines.append({'username': m['username'],
                           'text': m['text'],
                           'pub_date': m['pub_date']})
    # return json of the timelines with http status code 200
    return jsonify(timelines), 200

@mt_api.route('/public', methods=['GET'])
def public_timeline():
    """Displays the latest messages of all users."""
    messages=query_db('''
        select message.*, user.* from message, user
        where message.author_id = user.user_id
        order by message.pub_date desc limit ?''', [PER_PAGE])
        #make timeline list
        
    timelines = []
    for m in messages:
            timelines.append({'username': m['username'],
                           'text': m['text'],
                           'pub_date': m['pub_date']})
    # return json of the timelines with http status code 200
    return jsonify(timelines), 200

@mt_api.route('/<username>/timeline', methods=['GET'])
def user_timeline(username):
    #query the profile user for the next message
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': 'No such user'}), 404
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

@mt_api.route('/<username>/timeline', methods=['POST'])
def add_message(username):
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': 'No such user'}), 404

    testData = 'This is the test message'

    if testData == None:
        return jsonify({'Message': 'Empty'}), 400

    db = get_db()
    db.execute('''INSERT INTO message (author_id, text, pub_date)
                 VALUES (?,?,?)''', (userID, testData, int(time.time())))
    db.commit()
    return jsonify({'Message': 'Message was recorded'}), 200

@mt_api.route('/<username>/following', methods=['GET'])
def following(username):
    #query the profile user for the next message
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "No such User"}), 404

    people_following = query_db('''
                                select * from follower where
                                follower.who_id = ?''',
                                [userID])
    people = []
    for p in people_following:
        person = query_db('''select * from user where user_id = ?''',
                            [p['whom_id']])
        people.append({'followers': str(person[0]['username'])})
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
                            [p['who_id']])
        people.append({'followers': str(person[0]['username'])})
    return jsonify(followers=people), 200

@mt_api.route('/<username>/following', methods=['POST'])
def follow_user(username):
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "No such user"}), 404

    test = get_user_id('jeff')

    db = get_db()
    db.execute('''INSERT INTO FOLLOWER (who_id, whom_id)
                VALUES (?,?)''', [userID, test])
    db.commit()
    user = query_db('select username from user where user_id = ?',
                            [test])
    return jsonify({'Message': 'Following ' + str(user[0]['username'])}), 200

@mt_api.route('/<username>/following', methods=['DELETE'])
def unfollow_user(username):
    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "Unauthorized"}), 401

    userID = get_user_id(username)
    if userID == None:
        return jsonify({'Message': "No such user"}), 404

    test = get_user_id('jeff')

    db = get_db()
    db.execute('''DELETE FROM FOLLOWER WHERE who_id = ? and whom_id=?''',
                [userID, test])
    db.commit()

    user = query_db('select username from user where user_id = ?',
                            [test])
    return jsonify({'Message': 'Now unfollowing ' + str(user[0]['username'])}), 200
