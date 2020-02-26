import pika
import traceback


class Publiser:
    def __init__(self, host='localhost', port=None, exchange_name="", queue_name='queue'):
        self._host = host
        self._port = port
        self.exchange_name = exchange_name
        self.queue_name = queue_name

    def _create_connection(self):
        parameters = pika.ConnectionParameters(host=self._host)
        return pika.BlockingConnection(parameters)

    def publish(self, message):
        connection = None
        try:
            connection = self._create_connection()
            channel = connection.channel()
            channel.exchange_declare(exchange=self.exchange_name, passive=True)
            channel.basic_publish(exchange=self.exchange_name, routing_key=self.queue_name, body=message)
            print(" [x] Sent message %r" % message)
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise e
        finally:
            if connection:
                connection.close()