# -*- coding:utf-8 -*-
import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        #生成socket连接
        auth = pika.PlainCredentials('admin', 'admin')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='127.0.0.1', port=5672, virtual_host='my_vhost', credentials=auth))
        self.connection = connection
        #生成管道连接
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        # 不能直接使用此函数  不然会导致阻塞 要使用process_data_events 进行数据处理
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        print(self.callback_queue)
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,#从rpc_queue拿去结果 之后发送到self.callback_queuq 消费
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            print("process_data_events start")
            self.connection.process_data_events() #self.connection.process_data_events()会去队列中获取处理数据事件，当数据来临的时候，会直接去调用回调函数去处理数据
            print("process_data_events end")
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)