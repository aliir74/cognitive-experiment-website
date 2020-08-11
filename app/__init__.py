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
    try_to_answer = 1
    duplicate_user = mongo.db.users.find({'$or': [{'email': form_data.get('email')}]})
    if duplicate_user.count() != 0:
        user = duplicate_user[0]
        if user.get('complete', False):
            return {}, 409
        else:
            god_numbers = user['god_numbers']
            god_value = user['god_value']
            try_to_answer = user.get('try_to_answer', 1)+1
            mongo.db.users.update_one({'email': form_data.get('email')}, {
                '$set': {
                    'try_to_answer': try_to_answer
                }
            })
    else:
        mongo.db.users.insert_one({'email': form_data.get('email'),
                               'name': form_data.get('name'),
                               'mobile': form_data.get('mobile'),
                               'sex': form_data.get('sex'),
                               'age': int(form_data.get('age')),
                               'god_numbers': god_numbers,
                               'god_value': god_value,
                               'try_to_answer': try_to_answer,
                               'complete': False})
    return jsonify({'result': {
        'god_numbers': god_numbers,
        'god_value': god_value,
        'try_to_answer': try_to_answer
    }})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    mongo.db.users.update_one({'email': data['email']}, {
        "$set": {
            "dictator_value": int(data['dictator_value']),
            "after_change_value": [int(x) for x in data['after_change_value']],
            "judge_value": [int(x) for x in data['judge_value']],
            "iri_value": [(int(x) if x!='' else x) for x in data['iri_value']],
            "value": [int(x) for x in data['value']],
            "step_time": [x for x in data['step_time']],
            "help": int(data['help']),
            "complete": bool(data['complete']),
            "step_presence": [int(x) for x in data['step_presence']],
            "is_mobile": bool(data['is_mobile']),
            "dictator_again": int(data['dictator_again']),
            "step_sequence": data['step_sequence'],
            "send_time": data['send_time'],
            "step_change": data['step_change']
        }
    })
    return 'OK', 200

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


