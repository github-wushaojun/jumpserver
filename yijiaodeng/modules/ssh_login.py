#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

from modules import interactive
from modules import auditlog
from modules import auditlog_queue_producer

import paramiko
import datetime
import os

def ssh_login(auth_choice, private_key_path, username, hostip, hostport, remoteusername, remoteuserpass):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    if auth_choice == 'k':
        try:
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
            client.connect(hostip, hostport, remoteusername, pkey=private_key)
            client.get_transport().open_session().get_pty()
            chan = client.invoke_shell()
            print("\033[33;1m*** " + remoteusername + "用户ssh登录成功! ***\n\033[0m")
            # auditlog.auditlog(datetime.datetime.now(), username, hostip, remoteusername, "登录成功!")
            auditlog_queue_producer.send(datetime.datetime.now(), username, hostip, remoteusername, "登录成功!")
            interactive.interactive_shell(chan, username, hostip, remoteusername)
            chan.close()
            client.close()
        except Exception as e:
            print("\033[31;1m\n%s: %s\033[0m" % (remoteusername, e))
            try:
                client.close()
            except:
                pass
    else:
        try:
            client.connect(hostip,
                           hostport,
                           remoteusername,
                           remoteuserpass,
                           timeout=30)
            client.get_transport().open_session().get_pty()
            chan = client.invoke_shell()
            print("\033[33;1m*** " + remoteusername + "用户ssh登录成功! ***\n\033[0m")
            # auditlog.auditlog(datetime.datetime.now(), username, hostip, remoteusername, "登录成功!")
            auditlog_queue_producer.send(datetime.datetime.now(), username, hostip, remoteusername, "登录成功!")
            interactive.interactive_shell(chan, username, hostip, remoteusername)
            chan.close()
            client.close()
        except Exception as e:
            print("\033[31;1m\n%s: %s\033[0m" % (remoteusername, e))
            try:
                client.close()
            except:
                pass
