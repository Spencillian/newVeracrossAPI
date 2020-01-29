import os
import markdown
import shelve
from flask import request
from Crawler import Crawler

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("users")
    return db


@app.teardown_appcontext
def teardown_db(e):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + '/VeracrossAPI/README.md') as file:
        content = file.read()
        return markdown.markdown(content)


class UserList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        # users = []
        #
        # for key in keys:
        #     users.append(shelf[key])
        #
        # print(shelf[key])

        return {'message': "Success", 'data': keys}, 200

    def post(self):
        req_data = request.get_json()

        shelf = get_db()
        shelf[req_data['username']] = req_data

        c = Crawler()
        c.navigate(shelf[req_data['username']]['username'], shelf[req_data['username']]['password'])

        grades = c.get_grades()

        if not grades:
            return {'message': f"The username {shelf[req_data['username']]['username']} or password {shelf[req_data['username']]['password']} is incorrect"}, 400

        return {'message': "User Registered", 'data': grades}, 200


class User(Resource):
    def delete(self, username):
        shelf = get_db()

        if not (username in shelf):
            return {'message': f"User {username} not found", 'data': {}}, 404

        del shelf[username]
        return '', 204


api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<string:username>')

app.run(host='0.0.0.0', port='7777', debug=True)
