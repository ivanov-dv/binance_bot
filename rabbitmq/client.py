import time

import pika
from pika.exceptions import ConnectionClosedByBroker, StreamLostError

from loguru import logger


class RabbitMq:
    def __init__(self, host='localhost', port=5672, user='guest', password='guest',
                 vhost='/', queue_name='pet_tgbot_queue', exchange=''):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.vhost = vhost
        self.queue_name = queue_name
        self.exchange = exchange
        self.parameters = pika.URLParameters(f'amqp://{self.user}:{self.password}@{self.host}:{self.port}')
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def reconnect(self):
        self.parameters = pika.URLParameters(f'amqp://{self.user}:{self.password}@{self.host}:{self.port}')
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def send_message(self, message):
        try:
            self.channel.basic_publish(exchange=self.exchange,
                                       routing_key=self.queue_name,
                                       body=message,
                                       properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))
        except ConnectionClosedByBroker:
            time.sleep(1)
            logger.error("Connection closed by broker, attempting to reconnect")
            self.reconnect()
            self.send_message(message)
        except StreamLostError:
            time.sleep(1)
            logger.error("Stream lost error, attempting to reconnect")
            self.reconnect()
            self.send_message(message)
