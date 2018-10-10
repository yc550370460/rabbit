#!/usr/bin/env python
# coding=utf8
import pika
from contextlib import contextmanager


class Rabbit(object):
    def __init__(self, ip="localhost", queue="hello"):
        self.ip = ip
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        

def wrapper(cls):
    senders = dict()

    def inner(ip, queue):
        if senders.get(ip + "_" + queue, None) is None:
            senders[ip + "_" + queue] = cls(ip, queue)
        return senders[ip + "_" + queue]
    return inner


@wrapper
class RabbitSend(object):
    def __init__(self, ip, queue):
        self.ip = ip
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    @contextmanager
    def send(self, exchange, message):
        self.channel.basic_publish(exchange=exchange, routing_key=self.queue, body=message)
        yield
        self.close()

    def close(self):
        print "execute close()"
        self.connection.close()

if __name__ == "__main__":
    instance1 = RabbitSend("localhost", "hello")
    instance2 = RabbitSend("localhost", "hello")
    print id(instance1), id(instance2)
    with instance1.send("", "hello world2"), instance2.send("", "hello world2"):
        print "123"