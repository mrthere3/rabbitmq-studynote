# -*- coding:utf-8 -*-
import pika

# 连接服务器
auth = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',port=5672, virtual_host='my_vhost',credentials=auth))
channel = connection.channel()
# channel.queue_declare(queue='hello',durable= True) #durable 来确认这个队列持久化
# result = channel.queue_declare(queue='', exclusive=True) # exclusion 使用排他队列
channel.exchange_declare(exchange='logs', exchange_type='fanout')
message = "使用广播的方式发送"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(f"发送{message}")
channel.close()