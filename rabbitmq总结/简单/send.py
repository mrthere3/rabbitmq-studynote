# -*- coding:utf-8 -*-
import pika
auth = pika.PlainCredentials("admin","admin")
parameter = pika.ConnectionParameters(host='127.0.0.1',port=5672, virtual_host='my_vhost',credentials=auth)
connection = pika.BlockingConnection(parameter)
channel = connection.channel()
channel.queue_declare(queue="hello")
channel.basic_publish(exchange="",routing_key="hello",body="hello,world")
print("向rabbitmq发送hello world")
connection.close()
