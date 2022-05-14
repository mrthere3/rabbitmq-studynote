# -*- coding:utf-8 -*-

import pika
auth = pika.PlainCredentials("admin","admin")
parameter = pika.ConnectionParameters(host='127.0.0.1',port=5672, virtual_host='my_vhost',credentials=auth)
connection = pika.BlockingConnection(parameter)
channel = connection.channel()
channel.queue_declare(queue='hello',durable=True) #持久化队列
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(queue="hello",on_message_callback=callback,properties=pika.BasicProperties(delivery_mode=2)) #持久化队列的消息
print("开始监听消费")
channel.start_consuming()
