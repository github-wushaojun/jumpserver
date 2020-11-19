#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

from conf import conn_db_setting
from modules import list_hosts_remoteusers
from modules import update_tables

conn = conn_db_setting.engine.connect()

def func_print(my_name):
    print('''
[1] 查看%s用户可登录的所有主机列表
[2] 添加用户
[3] 添加用户组
[4] 添加主机
[5] 添加主机组
[6] 添加远程用户
[7] 添加授权策略
    ''' %(my_name))

def handler(signal, frame):
    pass

def login_check(my_name):
    # 查找用户是否存在
    find_user_cursor = conn.execute(
        "select * from users where username=%(username)s;", username=my_name
    )
    find_user_result = find_user_cursor.fetchall()
    if find_user_result:
        return True
    else:
        print("没有 %s 用户" % (my_name))
        return False

def function_menu_choice(my_name):
    if my_name != "":
        user_check_result = login_check(my_name)
        if user_check_result:
            while True:
                func_print(my_name)
                func_choice = input('请选择功能: ').strip()
                if func_choice.isdigit():
                    if int(func_choice) == 1:
                        list_hosts_remoteusers.main(my_name)
                    elif int(func_choice) == 2:
                        update_tables.create_users()
                    elif int(func_choice) == 3:
                        update_tables.create_usrgrp()
                    elif int(func_choice) == 4:
                        update_tables.create_hosts()
                    elif int(func_choice) == 5:
                        update_tables.create_hstgrp()
                    elif int(func_choice) == 6:
                        update_tables.create_remoteusers()
                    elif int(func_choice) == 7:
                        update_tables.create_authorization()
                    else:
                        print('编号输入有误!')
                else:
                    print('请输入数字！')