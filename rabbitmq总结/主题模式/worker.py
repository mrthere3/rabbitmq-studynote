# -*- coding:utf-8 -*-
import pika
auth = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',port=5672, virtual_host='my_vhost',credentials=auth,heartbeat=60))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue  #生产者可以不声明队列  但是消费者需要（在使用exchange进行转发的时候）
serect = "#.red.#"
channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=serect) #将exchange与queue进行绑定
def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True,)
channel.start_consuming()