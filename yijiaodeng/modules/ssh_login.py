#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

from modules import interactive
from modules import auditlog
from modules import auditlog_queue_producer

import sys, paramiko, datetime, struct, fcntl
import termios

def ssh_login(username, hostip, hostport, remoteusername, remoteuserpass):
    def get_win_size():
        if 'TIOCGWINSZ' in dir(termios):
            TIOCGWINSZ = termios.TIOCGWINSZ
        else:
            TIOCGWINSZ = '1074295912L'
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
        return struct.unpack('HHHH', x)[0:2]

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.connect(hostip,
                       hostport,
                       remoteusername,
                       remoteuserpass,
                       timeout=30)
        win_size = get_win_size()
        chan = client.invoke_shell(term='vt100', height=win_size[0], width=win_size[1])
        print("\033[33;1m*** " + remoteusername + "用户ssh登录成功! ***\n\033[0m")
        # auditlog.auditlog(datetime.datetime.now(), username, hostip, remoteusername, "登录成功!")
        try:
            auditlog_queue_producer.send(datetime.datetime.now(), username, hostip, remoteusername, "登录成功!")
        except Exception as e:
        # print('用户行为审计写入队列异常, 请检查队列服务器是否能够连接成功')
            pass
        interactive.interactive_shell(chan, username, hostip, remoteusername)
        chan.close()
        client.close()
    except Exception as e:
        print("\033[31;1m\n%s: %s\033[0m" % (remoteusername, e))
        try:
            client.close()
        except:
            pass