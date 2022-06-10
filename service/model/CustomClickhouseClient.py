import os
import time
from datetime import date, datetime
import logging
logging.basicConfig()

from clickhouse_driver import Client

database_name = os.environ["DATABASE"]


class CustomClickhouseClient(Client):
    def __init__(self, vectors_buffer_max_size: int = 100, *ch_client_args, **ch_client_kwargs):
        super().__init__(*ch_client_args, **ch_client_kwargs)
        self.vectors_buffer_max_size = vectors_buffer_max_size
        self.vectors_buffer = []
        self.logger = logging.getLogger("CH logger")
        self.logger.setLevel(logging.INFO)

    def create_dev_database(self):
        create_db_query = f"""
        CREATE DATABASE IF NOT EXISTS {database_name}
        """
        return self.execute(create_db_query)

    def create_dev_data_table(self):
        create_data_table_query = f"""
            CREATE TABLE IF NOT EXISTS {database_name}.query_logs
            (
                dt Date,
                ts DateTime,
                id String,
                vector String,
                meta1 String,
                meta2 String,
                meta3 int,
                meta4 int,
                meta5 String,
                meta6 String,
                prediction Nullable(int)
            )
            ENGINE = MergeTree
            PARTITION BY dt
            ORDER BY (ts, meta1)
        """
        return self.execute(create_data_table_query)

    def store_vector(self, vector: dict):
        vec_copy = vector.copy()
        vec_copy["dt"] = date.today()
        vec_copy["ts"] = datetime.now()
        if "prediction" not in vec_copy:
            vec_copy["prediction"] = None

        self.vectors_buffer.append(vec_copy)
        if len(self.vectors_buffer) >= self.vectors_buffer_max_size:
            self.logger.info(f"{len(self.vectors_buffer)} elements are stored in the buffer. "
                             f"Pushing it to the database.")
            result = self.execute(f"INSERT INTO {database_name}.query_logs (*) VALUES", self.vectors_buffer)
            self.logger.info(f"{result} elements are pushed successfully.")
            self.vectors_buffer.clear()

    def check_connection(self, attempts=5):
        self.logger.info("Checking connection")
        for i in range(attempts):
            self.logger.info(f"Attempt number {i}")
            try:
                self.execute('SHOW DATABASES')
            except EOFError:
                self.logger.info("Connection is failed...")
                time.sleep(30.0)
            else:
                return
        raise Exception("Model can't connect to the database!")
