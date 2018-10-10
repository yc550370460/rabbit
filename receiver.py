#!/usr/bin/env python
# coding=utf8
import pika
from sender import Rabbit
from contextlib import contextmanager


class RabbitRecv(Rabbit):
    def __init__(self, ip, queue):
        super(RabbitRecv, self).__init__(ip, queue)

    def callback(self, ch, method, properties, body):
        print " [x] Received %r" % (body,)

    @contextmanager
    def ready(self):
        print ' [*] Waiting for messages. To exit press CTRL+C'
        try:
            self.channel.basic_consume(self.callback, queue=self.queue, no_ack=True)
            yield self
        except Exception, e:
            raise e

    def start(self):
        self.channel.start_consuming()

if __name__ == "__main__":
    ra = RabbitRecv(ip="localhost", queue="hello")
    with ra.ready() as f:
        f.start()