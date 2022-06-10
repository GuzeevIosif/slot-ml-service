import pandas as pd
from flask import Flask, json

api = Flask(__name__)


@api.route("/<token>/token", methods=['GET'])
def get_token(token):
    return json.dumps({
        "token": token
    })


@api.route(f'/api/v1/users/<string:token>/vectors/', methods=['GET'])
def vectors(token):
    # We load data each time, therefore it will slow our response a bit.
    # Because real API won't response immediately
    data = pd.read_csv("data.csv")
    return json.dumps(data.sample().to_dict())


@api.route(f'/api/v1/users/<string:token>/results/', methods=['POST'])
def results(token):
    return json.dumps({
        "message": "class was stored successfully"
    })


@api.route(f'/api/v1/users/<string:token>/stats', methods=['GET'])
def stats(token):
    return json.dumps({
        'stats': [{
            'total_vectors': 306,
            'attempt_number': 1,
            'avg_false_positive_ratio': 4.44444,
            'avg_user_level': 1,
            'avg_spent_time': 1230.02,
            'total_results': 45,
            'avg_accuracy': 24.4444,
            'classify_data_ratio': 14.7059,
            'avg_false_negative_ratio': 60
        }]})


if __name__ == '__main__':
    api.run()
