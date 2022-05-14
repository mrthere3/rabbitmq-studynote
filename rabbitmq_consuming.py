# -*- coding:utf-8 -*-
import pika

# 连接服务器
auth = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',port=5672, virtual_host='my_vhost',credentials=auth))
channel = connection.channel()

# rabbitmq消费端仍然使用此方法创建队列。这样做的意思是：若是没有就创建。和发送端道理道理。目的是为了保证队列一定会有
channel.queue_declare(queue='hello')


# 收到消息后的回调
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue='hello',on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
