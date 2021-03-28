from flask import Flask, request,jsonify, make_response
from model.Model import configureMash, User, UserSchema
from model.Dao import save,load
import json

app = Flask('API_Cotacao')


@app.route('/', methods=['GET'])
def index():
    return  jsonify(msg='Server is running...')

@app.route('/users/', methods=['GET'])
def users():
    bs = UserSchema(many=True)
    result = load()
    response = bs.jsonify(result)
    return make_response(response, 200)


@app.route('/users/add', methods=['POST'])
def usersAdd():
    try:
        json_dict = request.get_json()
        user = User(**json_dict)
        new = save(user)
        json_dict
        return make_response(f'id: {new.id}', 200)
    except Exception as e:
        print(e)
        return  {'Error'}


configureMash(app)
app.run()