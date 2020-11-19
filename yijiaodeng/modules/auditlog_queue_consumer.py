#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import conn_db_setting
import pika
import json

conn = conn_db_setting.engine.connect()

def receive():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs_fanout', exchange_type='fanout', durable=True)
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs_fanout', queue=queue_name)

    def callback(ch, method, properties, body):
        body_new=json.loads(body)
        print('body: %s' %body_new)
        insert_cursor = conn.execute(
            "insert into auditlog(time,username,hostip,remoteusername,content)values(%(time)s,%(username)s,%(hostip)s,%(remoteusername)s,%(content)s);",
            time=body_new['time'], username=body_new['username'], hostip=body_new['hostip'], remoteusername=body_new['remoteusername'], content=body_new['content']
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue_name, callback, False)

    print('Waiting for messages...')
    channel.start_consuming()

if __name__ == "__main__":
    receive()