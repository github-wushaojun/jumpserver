#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

import socket
import sys
import datetime
from paramiko.py3compat import u
from modules import auditlog
from modules import auditlog_queue_producer
import os

# windows does not have termios...
try:
    import termios
    import tty

    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan, username, hostip, remoteusername):
    if has_termios:
        posix_shell(chan, username, hostip, remoteusername)
    else:
        windows_shell(chan)

def posix_shell(chan, username, hostip, remoteusername):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        cmd = []
        tab_key = False
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if tab_key:
                        if x not in ('\x07', '\r\n'):
                            cmd.append(x)
                        tab_key = False
                    if len(x) == 0:
                        sys.stdout.write("\033[31;1m\r\n已退出" + remoteusername + "用户ssh登录!\r\n\033[0m")
                        try:
                            auditlog_queue_producer.send(datetime.datetime.now(), username, hostip, remoteusername, "退出登录!")
                        except Exception as e:
                            #print('用户行为审计写入队列异常, 请检查队列服务器是否能够连接成功')
                            pass
                        # auditlog.auditlog(datetime.datetime.now(), username, hostip, remoteusername,"退出登录!")
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = (os.read(sys.stdin.fileno(), 4096)).decode()
                if x != '\r':
                    cmd.append(x)
                else:
                    cmd_str=''.join(cmd)
                    if cmd_str != "":
                        #auditlog.auditlog(datetime.datetime.now(), username, hostip, remoteusername, cmd_str)
                        try:
                            auditlog_queue_producer.send(datetime.datetime.now(), username, hostip, remoteusername, cmd_str)
                        except Exception as e:
                            #print('用户行为审计写入队列异常, 请检查队列服务器是否能够连接成功')
                            pass
                    cmd.clear()
                if x == '\t':
                    tab_key = True
                if len(x) == 0:
                    break
                chan.send(x)
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")

    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
