#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

import os, sys

from conf import conn_db_setting
import pika
import json

conn = conn_db_setting.engine.connect()

def send(time,username,hostip,remoteusername,content):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs_fanout', exchange_type='fanout', durable=True)

    message = {
        "time":str(time),
        "username":username,
        "hostip":hostip,
        "remoteusername":remoteusername,
        "content":content
        }

    channel.basic_publish(exchange='logs_fanout',
                          routing_key='',
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          )
                          )
    connection.close()