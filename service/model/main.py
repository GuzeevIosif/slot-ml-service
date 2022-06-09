import os
import logging
import time
logging.basicConfig()

import requests

from CustomClickhouseClient import CustomClickhouseClient
from Predictor import Predictor


TRAFFIC_URL = os.environ["TRAFFIC_URL"]
CH_URL =  os.environ["CH_URL"]
CH_PORT = os.environ["CH_PORT"]
USER_TOKEN = os.environ["USER_TOKEN"]


class TrafficLoader:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get_new_vector(self):
        api = f"/api/v1/users/{self.token}/vectors/?random"
        print(self.url + api)
        while True:
            response = requests.get(self.url+api)
            print(response.status_code)
            if response.status_code == 200:
                break
            else:
                time.sleep(0.1)
        return response

    def post_prediction(self, vec_id, predicted_class):
        api = f"/api/v1/users/{self.token}/results/"
        response = requests.post(self.url + api, data={"vector": vec_id, "class": predicted_class})
        return response


if __name__ == '__main__':
    logger = logging.getLogger("Main-logger")
    logger.setLevel(logging.INFO)
    ch_client = CustomClickhouseClient(vectors_buffer_max_size=1, host=CH_URL, port=CH_PORT)
    ch_client.check_connection()

    traffic_loader = TrafficLoader(TRAFFIC_URL, USER_TOKEN)
    predictor = Predictor()

    # Create if not exists
    ch_client.create_dev_database()
    ch_client.create_dev_data_table()
    logger.info("Service is started")

    while True:
        resp = traffic_loader.get_new_vector().json()
        logger.info(f"Got new query: {resp}")

        prediction = predictor.predict([resp])[0]
        print(resp["id"], prediction)
        logger.info(f'Prediction is pushed. Response: {traffic_loader.post_prediction(resp["id"], prediction).json()}')
        resp["prediction"] = prediction

        ch_client.store_vector(resp)
        time.sleep(1.0)
