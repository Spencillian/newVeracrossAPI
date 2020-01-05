import os
import markdown
import shelve
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
        parser = reqparse.RequestParser()

        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()

        shelf = get_db()
        shelf[args['username']] = args

        return {'message': "User Registered", 'data': args['username']}, 201


class User(Resource):
    def get(self, username):
        shelf = get_db()

        if not (username in shelf):
            return {'message': f"User {username} not found", 'data': {}}, 404

        c = Crawler()
        print(shelf[username]['password'])
        c.navigate(shelf[username]['username'], shelf[username]['password'])
        grades = c.get_grades(6)
        print(grades)

        return {'message': 'User found', 'data': grades}, 200

    def delete(self, username):
        shelf = get_db()

        if not (username in shelf):
            return {'message': f"User {username} not found", 'data': {}}, 404

        del shelf[username]
        return '', 204


api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<string:username>')

app.run(host='0.0.0.0', port='7777', debug=True)
