import os
import sys

from dotenv import load_dotenv
from loguru import logger
from datetime import datetime

from db.db import RedisDB
from utils.mailer import EmailSMTP


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# LOGGER SETTINGS
logger.configure(
    handlers=[
        dict(sink=sys.stderr, level=0),
        dict(sink=f"logs/{datetime.now().strftime('%Y-%m-%d')}.log",
             rotation="1024 KB",
             retention=10,
             compression="zip")
    ]
)

# MAILER SETTINGS
SENDER = "sender@mail.com"
RECIPIENT = "recipient@mail.com"
SMTP_SERVER = "smtp.mail.com"
SMTP_PORT = 465

# BOT SETTINGS
TARGET_PERCENT = 28
MONITORING_TIMEOUT = 120
MONITORING_OPEN_ORDERS_TIMEOUT = 1
MONITORING_NOTICE_TIMEOUT = 1
TRY_TIMEOUT_IF_EXCEPT = 15
AMOUNT_GENERAL_ITERATIONS = 100
TARGET_RATIO_FOR_OPEN_ORDERS = 0.87

# DB SETTINGS
HOST_REDIS = os.getenv("HOST_REDIS", "localhost")
PORT_REDIS = os.getenv("PORT_REDIS", 6379)
DATABASE_REDIS = os.getenv("DATABASE_REDIS", 0)
PASSWORD_REDIS = os.getenv("PASSWORD_REDIS", "<PASSWORD>")

HOST_RABBIT = os.getenv("HOST_RABBIT", "localhost")
USER_RABBIT = os.getenv("USER_RABBIT", "user")
PASSWORD_RABBIT = os.getenv("PASSWORD_RABBIT", "password")

db_client = RedisDB(HOST_DB, PORT_REDIS, DATABASE_REDIS, PASSWORD_REDIS)
mailer = EmailSMTP(SMTP_SERVER, SMTP_PORT, SENDER, RECIPIENT, os.getenv("MAIL_PASSWORD"))
