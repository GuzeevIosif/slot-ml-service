import os
from flask import Flask, json

api = Flask(__name__)


@api.route("/<token>/token", methods=['GET'])
def get_token(token):
    return json.dumps({
        "token": token
    })


@api.route(f'/api/v1/users/<string:token>/vectors/', methods=['GET'])
def vectors(token):
    return json.dumps({
        'meta1': 'REQUEST_ARGS',
        'id': '27457723e25d71932c9f229ed52cae02',
        'meta2': 'action',
        'vector': 'profile;area=statistics;u=966409',
        'meta3': 200,
        'meta6': '157.55.39.237',
        'meta4': 372,
        'meta5': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    })


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
