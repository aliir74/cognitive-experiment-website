import os
from flask import Flask, current_app, send_file
from flask import jsonify, request
from .api import api_bp
from .client import client_bp
from flask_pymongo import PyMongo
import random


app = Flask(__name__, static_folder='../dist/static')
app.config['MONGO_DBNAME'] = 'cognitive'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/cognitive'
mongo = PyMongo(app)

app.register_blueprint(api_bp)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/cognitive"
# mongo = PyMongo(app)
# app.register_blueprint(client_bp)

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

@app.route('/texts', methods=['GET'])
def get_texts():
    res = []
    for t in mongo.db.text.find():
        res.append({'name': t['name'], 'text': t['text']})
    return jsonify({'result': res})

@app.route('/register', methods=['POST'])
def register():
    form_data = request.get_json().get('person')
    god_numbers = [x*10 for x in range(0, 10)]
    random.shuffle(god_numbers)
    values = [100, 200, 400]
    god_value = values[random.randint(0, 2)]
    duplicate_user = mongo.db.users.find({'$or': [{'email': form_data.get('email')}, {'mobile': form_data.get('mobile')}]}).count()
    if duplicate_user != 0:
        return {}, 409
    mongo.db.users.insert_one({'email': form_data.get('email'),
                               'name': form_data.get('name'),
                               'mobile': form_data.get('mobile'),
                               'god_numbers': god_numbers,
                               'god_value': god_value})
    return jsonify({'result': {
        'god_numbers': god_numbers,
        'god_value': god_value
    }})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    mongo.db.users.update_one({'email': data['email']}, {
        "$set": {
            "dictator_value": int(data['dictator_value']),
            "after_change_value": [int(x) for x in data['after_change_value']],
            "judge_value": [int(x) for x in data['judge_value']],
            "iri_value": [int(x) for x in data['iri_value']],
            "value": [int(x) for x in data['value']],
            "step_time": [int(x) for x in data['step_time']],
            "help": int(data['help'])
        }
    })
    return 'OK', 200

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


