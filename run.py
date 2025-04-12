from threading import Thread

from engine import *


@logger.catch
def main():
    db_client.update_list_pairs(pairs.get_all_pairs())
    rabbit.send_message(f"{datetime.now()} Запуск")
    logger.trace("Запуск")
    task1 = Thread(target=monitoring_pairs_bot.start_general_monitoring_pairs)
    task2 = Thread(target=monitoring_open_orders_bot.start_monitoring_open_orders)
    task1.start()
    task2.start()


if __name__ == "__main__":
    main()
