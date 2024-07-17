import time

from engine import *
from status import StatusMonitoringPairs


class MonitoringPairs:
    def __init__(self, client_bot, mailer_client, rabbit_client, db, target_percent, general_amount_iterations):
        self.client = client_bot
        self.mailer = mailer_client
        self.rabbit = rabbit_client
        self.db = db
        self.target_percent: int = target_percent
        self.general_amount_iterations: int = general_amount_iterations
        self.list_pairs: list = []
        self.status: StatusMonitoringPairs = StatusMonitoringPairs(
            "MonitoringPairs",
            amount_pairs=len(self.list_pairs),
            target_percent=target_percent
        )

    def get_list_symbols(self):
        self.list_pairs = self.db.get_list_pairs()

    def monitoring_list_pairs(self):
        for pair in self.list_pairs:
            try:
                prices = self.client.futures_ticker(symbol=pair)
                fact_percent_change = float(prices['priceChangePercent'])
            except KeyError:
                logger.trace(f'Некорректная пара. Удаление {pair} из списка')
                self.list_pairs.remove(pair)
                continue
            except Exception as _ex:
                logger.error(f'Ошибка {_ex}. Повтор через {TRY_TIMEOUT_IF_EXCEPT} секунд')
                time.sleep(TRY_TIMEOUT_IF_EXCEPT)
                continue
            else:
                if fact_percent_change > self.target_percent:
                    logger.info(f"Изменение {pair} на {prices['priceChangePercent']}%")
                    self.list_pairs.remove(pair)
                    self.rabbit.send_message(
                        f"{pair} больше {self.target_percent}% ({fact_percent_change}%)\n"
                        f"{datetime.now()}\nИзменение {pair} на {prices['priceChangePercent']}%"
                    )
                    self.mailer.send_email_message(
                        f"{pair} больше {self.target_percent}% ({fact_percent_change}%)",
                        f"{datetime.now()}\nИзменение {pair} на {prices['priceChangePercent']}%"
                    )
        self.status.slave_iteration_count += 1
        self.status.amount_pairs = len(self.list_pairs)

    def start_general_monitoring_pairs(self):

        while True:

            self.get_list_symbols()

            for iteration in range(self.general_amount_iterations):
                self.monitoring_list_pairs()
                db_client.update_monitoring_pairs_data(
                    self.status.name,
                    self.status.amount_pairs,
                    self.status.master_iteration_count,
                    self.status.slave_iteration_count,
                    self.status.target_percent
                )
                time.sleep(MONITORING_TIMEOUT)

            self.status.master_iteration_count += 1
