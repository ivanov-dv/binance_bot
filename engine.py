import sentry_sdk
from binance import Client

from config import *
from monitoring_pairs.get_pairs import Pairs
from monitoring_pairs.monitoring_pairs import MonitoringPairs
from monitoring_open_orders.monitoring_open_orders import MonitoringOpenOrders
from rabbitmq.client import RabbitMq

client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET"))
rabbit = RabbitMq(host=HOST_RABBIT, user=USER_RABBIT, password=PASSWORD_RABBIT)

monitoring_pairs_bot = MonitoringPairs(
    client, mailer, rabbit, db_client, TARGET_PERCENT, AMOUNT_GENERAL_ITERATIONS
)

monitoring_open_orders_bot = MonitoringOpenOrders(
    client, mailer, db_client
)

pairs = Pairs(client)

if SENTRY_DSN:
    sentry_sdk.init(SENTRY_DSN)

