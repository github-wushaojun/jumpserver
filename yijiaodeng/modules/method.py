#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

from conf import conn_db_setting
from modules import list_hosts_remoteusers
from modules import update_tables
import signal
import hashlib
import logging
import os

conn = conn_db_setting.engine.connect()

continue_flag = False

def func_role_print(my_name,role):
    print("\033[34;1m\n欢迎 %s 登录一脚登跳板机, 请开始你的表演！\033[0m" %(my_name))
    if role == 'admin':
        print('''
        [1] 查看可登录的所有主机列表
        [2] 添加用户
        [3] 添加用户组
        [4] 添加主机
        [5] 添加主机组
        [6] 添加远程用户
        [7] 添加授权策略
        ''')
    elif role == 'user':
        print('''
        [1] 查看可登录的所有主机列表
        ''')

def signal_all(*args):
    def handler(signal, frame):
        pass
    for s in args:
        signal.signal(s, handler)

def pass_md5_calculate(password):
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()

#暂时没有使用
def log_file_record(log_file_name,log_content,log_level):
    logger = logging.getLogger(log_file_name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/tmp/'+log_file_name+'log')
    fh.setLevel(log_level)
    fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)
    logger.info(log_content)

def login_check():
    while True:
        signal_all(signal.SIGQUIT, signal.SIGINT, signal.SIGTSTP)
        try:
            my_name = input("\033[32;1m请输入用户名: \033[0m").strip()
            my_pass = input("\033[32;1m请输入密码: \033[0m").strip()
            my_pass_md5_result=pass_md5_calculate(bytes(my_pass,encoding='utf-8'))

            # 查找用户是否存在
            find_cursor = conn.execute(
                "select username,userpass,role,status from users where username=%(username)s and userpass=%(userpass)s;", username=my_name,userpass=my_pass_md5_result
            )
            find_result = find_cursor.fetchall()
            if find_result:
                function_menu_choice(my_name, find_result[0][2], find_result[0][3])
                if continue_flag == True:
                    continue
            else:
                print("\033[31;1m用户名或密码错误, 请重新输入!\n\033[0m")
                continue
        except EOFError as e:
            print("\033[31;1m\n已退出登录!\n\033[0m")
            os._exit(0)

def function_menu_choice(my_name,role,status):
        while True:
            if status == 'start':
                func_role_print(my_name, role)
                if role == 'admin':
                    func_choice = input('请选择功能, ctrl+d退出登录: ').strip()
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
                            print("\033[31;1m编号输入有误!\033[0m")
                            continue
                    else:
                        print("\033[31;1m请输入数字！\033[0m")
                        continue
                elif role == 'user':
                    func_choice = input('请选择功能, ctrl+d退出登录: ').strip()
                    if func_choice.isdigit():
                        if int(func_choice) == 1:
                            list_hosts_remoteusers.main(my_name)
                        else:
                            print("\033[31;1m编号输入有误!\033[0m")
                            continue
                    else:
                        print("\033[31;1m请输入数字！\033[0m")
                        continue
                else:
                    print("\033[31;1mERROR: " + my_name + "用户异常, 未知的用户角色, 请联系管理员!\n\033[0m")
                    continue_flag == True
                    break
            elif status == 'stop':
                print("\033[31;1mERROR: " + my_name + "用户已被禁用, 请联系管理员!\n\033[0m")
                continue_flag == True
                break
            else:
                print("\033[31;1mERROR: " + my_name + "用户异常, 未知的用户状态, 请联系管理员!\n\033[0m")
                continue_flag == True
                break