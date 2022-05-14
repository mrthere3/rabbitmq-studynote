# -*- coding:utf-8 -*-
import pika

#连接队列服务器

auth = pika.PlainCredentials('admin','admin')
parameters = pika.ConnectionParameters(host='127.0.0.1',port=5672, virtual_host='my_vhost',credentials=auth)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

#创建队列。有就不管，没有就自动创建
channel.queue_declare(queue='hello')

#使用默认的交换机发送消息。exchange为空就使用默认的
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()