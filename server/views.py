import sqlite3
import bcrypt

from flask import request, jsonify, session

from server import app
from db import query_db


@app.route('/api/new', methods=['POST', 'GET'])
def new_listing():
  return str(request.get_json())


@app.route('/api/all')
def all_listings():
  listings = query_db('SELECT * FROM listings')
  return jsonify(listings)


@app.route('/api/register', methods=['POST'])
def register():
  if not request.json or not 'username' in request.json or not 'password' in request.json:
    abort(400)

  user = query_db('SELECT * FROM users WHERE username = ?',
                  request.json['username'], one=True)

  if user is not None:
    # TODO: report user already exists
    return ""

  hashed = bcrypt.hashpw(password, bcrypt.gensalt())

  query_db('INSERT INTO users (username,password) VALUES (?,?)',
           (request.json['username'], hashed))

  # TODO: return okay
  return ""

@app.route('/api/login', methods=['POST'])
def login():
  if not request.json or not 'username' in request.json or not 'password' in request.json:
    abort(400)


  user = query_db('SELECT * FROM users WHERE username = ?',
                  request.json['username'], one=True)

  if user is None:
    # TODO: report wrong username
    return ""

  if bcrypt.checkpw(request.json['password'], user['password']):
    # login successful
    session["user_id"] = user["id"]
    return jsonify({'result': 'success'})

  # TODO: return wrong password
  return ""

@app.route('/api/logout')
def logout():
  session.pop('user_id', None)
  return jsonify({'result': 'success'})


@app.route('/api/me')
def me():
  if 'user_id' in session:
    return jsonify({'status': 'LoggedIn'})
  return jsonify({'status': ''})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  """
  Catch all that redirects to index.html for the single page application
  """
  return app.send_static_file('index.html')