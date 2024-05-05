from binance import Client

from config import *
from monitoring_pairs.monitoring_pairs import MonitoringPairs
from monitoring_open_orders.monitoring_open_orders import MonitoringOpenOrders

client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET"))

monitoring_pairs_bot = MonitoringPairs(
    client, mailer, db_client, TARGET_PERCENT, AMOUNT_GENERAL_ITERATIONS
)

monitoring_open_orders_bot = MonitoringOpenOrders(
    client, mailer, db_client
)
