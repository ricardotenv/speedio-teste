import os
import ast
import pika
from database import MongoDBInstance

mongo = MongoDBInstance()

connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('HOST')))
channel = connection.channel()
channel.exchange_declare(exchange=os.getenv('EXCHANGE_NAME'),)
channel.queue_declare(queue=os.getenv('QUEUE_NAME'))
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.queue_bind(
    queue=os.getenv('QUEUE_NAME'),
    exchange=os.getenv('EXCHANGE_NAME'),
    routing_key=os.getenv('ROUTING_KEY')
)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    body = ast.literal_eval(body.decode('utf-8'))
    mongo.insert_one(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=os.getenv('QUEUE_NAME'), on_message_callback=callback, auto_ack=False)
channel.start_consuming()
