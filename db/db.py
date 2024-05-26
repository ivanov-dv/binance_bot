import pickle
import redis

from config import *


class RedisDB:
    def __init__(self, host, port, database):
        self.connection = redis.Redis(host=host, port=port, db=database)

    def update_monitoring_pairs_data(self,
                                     name_bot,
                                     amount_pairs,
                                     master_iteration_count,
                                     slave_iteration_count,
                                     target_percent) -> None:
        data = {
            "#": name_bot,
            "Количество пар": amount_pairs,
            "Цикл": master_iteration_count,
            "Подцикл": slave_iteration_count,
            "MIN процент": target_percent,
            "time_update_1": datetime.now()
        }
        serialize_data = pickle.dumps(data)
        self.connection.set(name_bot, serialize_data)

    def update_monitoring_open_orders_data(self,
                                           name_bot,
                                           amount_open_positions,
                                           open_orders_info) -> None:
        data = {
            "#": name_bot,
            "Открыто позиций": amount_open_positions,
            "time_update_2": datetime.now()
        }
        self.connection.set(name_bot, pickle.dumps(data))
        self.connection.set("open_orders_info", pickle.dumps(open_orders_info))

    def update_list_pairs(self, list_pairs):
        serialize_data = pickle.dumps(list_pairs)
        self.connection.set("list_pairs", serialize_data)

    def get_list_pairs(self):
        return pickle.loads(self.connection.get("list_pairs"))
