# -*- coding:utf-8 -*-
import pika

#创建socket
auth = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',port=5672, virtual_host='my_vhost',credentials=auth))

#获取通道
channel = connection.channel()

#生成队列
channel.queue_declare(queue='rpc_queue')


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)
    print(response)
    print(props.reply_to)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()