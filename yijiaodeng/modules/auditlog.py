#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

import os, sys

from conf import conn_db_setting

conn = conn_db_setting.engine.connect()

#直接写入数据库
def auditlog(time,username,hostip,remoteusername,content):

    insert_cursor = conn.execute(
        "insert into auditlog(time,username,hostip,remoteusername,content)values(%(time)s,%(username)s,%(hostip)s,%(remoteusername)s,%(content)s);",
        time=time, username=username, hostip=hostip, remoteusername=remoteusername, content=content
    )
