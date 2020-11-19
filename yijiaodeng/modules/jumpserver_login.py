#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

from modules import method
import signal

def login():
    while True:
        for s in signal.SIGQUIT,signal.SIGINT,signal.SIGTSTP:
            signal.signal(s, method.handler)
        try:
            my_name = input('请输入用户名: ').strip()
            method.function_menu_choice(my_name)
        except EOFError as e:
            print('\r')
            continue