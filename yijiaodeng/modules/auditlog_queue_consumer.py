#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import conn_db_setting

import pika
import json
import sys

def receive():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs_fanout', exchange_type='fanout', durable=True)
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs_fanout', queue=queue_name)

    def callback(ch, method, properties, body):
        global body_log_file_out
        body_new=json.loads(body)

        sys.stdout.write('body %s\n' %body_new)
        sys.stdout.flush()
        conn = conn_db_setting.engine.connect()
        insert_cursor = conn.execute(
            "insert into auditlog(time,username,hostip,remoteusername,content)values(%(time)s,%(username)s,%(hostip)s,%(remoteusername)s,%(content)s);",
            time=body_new['time'], username=body_new['username'], hostip=body_new['hostip'], remoteusername=body_new['remoteusername'], content=body_new['content']
        )
        insert_cursor.close()
        conn.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue_name, callback, False)

    sys.stdout.write('Waiting for messages...\n')
    sys.stdout.flush()
    channel.start_consuming()

if __name__ == "__main__":
    receive()