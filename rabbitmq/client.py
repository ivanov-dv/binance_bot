import pika


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
        self.parameters = pika.URLParameters(f'amqp://{user}:{password}@{host}:{port}')
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def send_message(self, message):
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.queue_name,
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))
