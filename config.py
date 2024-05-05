import os
import sys

from dotenv import load_dotenv
from loguru import logger
from datetime import datetime

from db.db import DB
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
TARGET_PERCENT = 10
MONITORING_TIMEOUT = 120
MONITORING_OPEN_ORDERS_TIMEOUT = 30
TRY_TIMEOUT_IF_EXCEPT = 15
AMOUNT_GENERAL_ITERATIONS = 100
TARGET_RATIO_FOR_OPEN_ORDERS = 0.87

# DB SETTINGS
HOST_DB = "127.0.0.1"
NAME_DB = "name_db"

db_client = DB(HOST_DB, os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), NAME_DB, autocommit=True)
mailer = EmailSMTP(SMTP_SERVER, SMTP_PORT, SENDER, RECIPIENT, os.getenv("MAIL_PASSWORD"))
