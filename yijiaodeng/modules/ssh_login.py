#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

from modules import interactive
from modules import auditlog
from modules import auditlog_queue_producer

import paramiko
import datetime

def ssh_login(username, hostip, hostport, remoteusername, remoteuserpass):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.connect(hostip,
                       hostport,
                       remoteusername,
                       remoteuserpass,
                       timeout=30)
        chan = client.invoke_shell()
        print("\033[33;1m*** " + remoteusername + "用户ssh登录成功! ***\n\033[0m")
        # auditlog.auditlog(datetime.datetime.now(), username, hostip, remoteusername, "登录成功!")
        auditlog_queue_producer.send(datetime.datetime.now(), username, hostip, remoteusername, "登录成功!")
        interactive.interactive_shell(chan, username, hostip, remoteusername)
        chan.close()
        client.close()

    except Exception as e:
        print('%s: %s' % (remoteusername, e))
        try:
            client.close()
        except:
            pass