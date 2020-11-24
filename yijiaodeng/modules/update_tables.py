#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import yaml
from modules import method
from conf import conn_db_setting

conn = conn_db_setting.engine.connect()

#用户+用户组
def select_users_table(username):
    select_users_table = conn.execute(
        "select userid from users where username=%(username)s", username=username
    )
    select_users_result = select_users_table.fetchall()
    if select_users_result:
        userid, = select_users_result[0]
        return userid

def insert_users_table(username, userpass, role='user', status='start'):
    insert_users_table = conn.execute(
        "insert into users(username,userpass,role,status)values(%(username)s,%(userpass)s,%(role)s,%(status)s)", username=username, userpass=userpass, role=role, status=status
    )

def select_usrgrp_table(usrgrpname):
    select_usrgrp_table = conn.execute(
        "select usrgrpid from usrgrp where usrgrpname=%(usrgrpname)s", usrgrpname=usrgrpname
    )
    select_usrgrp_result = select_usrgrp_table.fetchall()
    if select_usrgrp_result:
        result, = select_usrgrp_result[0]
        return result

def insert_usrgrp_table(usrgrpname):
    insert_usrgrp_table = conn.execute(
            "insert into usrgrp(usrgrpname)values(%(usrgrpname)s)", usrgrpname=usrgrpname
    )

def select_users_groups_table(userid, usrgrpid):
    select_users_groups_table = conn.execute(
        "select userid,usrgrpid from users_groups where userid=%(userid)s and usrgrpid=%(usrgrpid)s", userid=userid,
        usrgrpid=usrgrpid
    )
    select_users_groups_result = select_users_groups_table.fetchall()
    if select_users_groups_result:
        result = select_users_groups_result[0]
        return result

def insert_users_groups_table(userid, usrgrpid):
    insert_users_groups_table = conn.execute(
        "insert into users_groups(userid,usrgrpid)values(%(userid)s,%(usrgrpid)s)", userid=userid, usrgrpid=usrgrpid
    )


##主机+主机组
def select_hosts_table(hostip):
    select_hosts_table = conn.execute(
        "select hostid from hosts where hostip=%(hostip)s", hostip=hostip
    )
    select_hosts_result = select_hosts_table.fetchall()
    if select_hosts_result:
        hostid, = select_hosts_result[0]
        return hostid

def insert_hosts_table(hostip, hostport=22):
    insert_hosts_table = conn.execute(
        "insert into hosts(hostip,hostport)values(%(hostip)s,%(hostport)s)", hostip=hostip, hostport=hostport
    )

def select_hstgrp_table(hstgrpname):
    select_hstgrp_table = conn.execute(
        "select hstgrpid from hstgrp where hstgrpname=%(hstgrpname)s", hstgrpname=hstgrpname
    )
    select_hstgrp_result = select_hstgrp_table.fetchall()
    if select_hstgrp_result:
        result, = select_hstgrp_result[0]
        return result

def insert_hstgrp_table(hstgrpname):
    insert_hstgrp_table = conn.execute(
            "insert into hstgrp(hstgrpname)values(%(hstgrpname)s)", hstgrpname=hstgrpname
    )

def select_hosts_groups_table(hostid, hstgrpid):
    select_hosts_groups_table = conn.execute(
        "select hostid,hstgrpid from hosts_groups where hostid=%(hostid)s and hstgrpid=%(hstgrpid)s", hostid=hostid,
        hstgrpid=hstgrpid
    )
    select_hosts_groups_result = select_hosts_groups_table.fetchall()
    if select_hosts_groups_result:
        result = select_hosts_groups_result[0]
        return result

def insert_hosts_groups_table(hostid, hstgrpid):
    insert_hosts_groups_table = conn.execute(
        "insert into hosts_groups(hostid,hstgrpid)values(%(hostid)s,%(hstgrpid)s)", hostid=hostid, hstgrpid=hstgrpid
    )

#远程用户
def select_remoteusers_table(remoteusername):
    select_remoteusers_table = conn.execute(
        "select remoteuserid from remoteusers where remoteusername=%(remoteusername)s", remoteusername=remoteusername
    )
    select_remoteusers_result = select_remoteusers_table.fetchall()
    if select_remoteusers_result:
        result, = select_remoteusers_result[0]
        return result

def insert_remoteusers_table(remoteusername,remoteuserpass):
    insert_remoteusers_table = conn.execute(
        "insert into remoteusers(remoteusername,remoteuserpass)values(%(remoteusername)s,%(remoteuserpass)s)", remoteusername=remoteusername,remoteuserpass=remoteuserpass
    )

#授权策略
def select_authorization_table(authorizationname):
    select_authorization_table = conn.execute(
        "select authorizationname from authorization where authorizationname=%(authorizationname)s", authorizationname=authorizationname
    )
    select_authorization_result = select_authorization_table.fetchall()
    if select_authorization_result:
        result, = select_authorization_result[0]
        return result

def insert_authorization_table(authorizationname,userid,usrgrpid,hostid,hstgrpid,remoteuserid):
    insert_authorization_table = conn.execute(
        "insert into authorization(authorizationname,userid,usrgrpid,hostid,hstgrpid,remoteuserid)values(%(authorizationname)s,%(userid)s,%(usrgrpid)s,%(hostid)s,%(hstgrpid)s,%(remoteuserid)s)", authorizationname=authorizationname,userid=userid,usrgrpid=usrgrpid,hostid=hostid,hstgrpid=hstgrpid,remoteuserid=remoteuserid
    )

def create_users():
    file_path=BASE_DIR+"/conf/db_tables_yaml/users.yaml"
    with open(file_path,'r') as users_yaml_file:
        data=yaml.load(users_yaml_file, Loader=yaml.FullLoader)
    if data:
            for k,v in data.items():
                print('----------')
                if len(str(v['username'])) > 20 or len(str(v['userpass'])) > 20:
                    print('用户名和密码长度不能大于20个字符, 请检查'+v['username']+'和'+v['userpass']+'的长度!')
                    continue
                else:
                    v['userpass'] = method.pass_md5_calculate(bytes(str(v['userpass']),encoding='utf-8'))
                    if v.get('usrgrpname'):
                            usrgrpid=select_usrgrp_table(v['usrgrpname'])
                            if usrgrpid:
                                userid = select_users_table(v['username'])
                                if userid:
                                    print("\033[31;1m"+v['username'] + "(userid:" + str(userid) + ")" + " 已存在于users表, 无需添加!\033[0m")
                                else:
                                    if v.get('role'):
                                        if v['role'] == 'admin' or v['role'] == 'user':
                                            if v.get('status'):
                                                if v['status'] == 'start' or v['status'] == 'stop':
                                                    insert_users_table(username=v['username'],userpass=v['userpass'],role=v['role'],status=v['status'])
                                                else:
                                                    print("\033[31;1m" + v['username'] + "指定了" + "未知的状态" + v['status'] + ", 请修改后重新添加!\033[0m")
                                                    continue
                                            else:
                                                insert_users_table(username=v['username'], userpass=v['userpass'], role=v['role'])
                                        else:
                                            print("\033[31;1m"+v['username'] + "指定了" + "未知的角色" + v['role'] + ", 请修改后重新添加!\033[0m")
                                            continue
                                    else:
                                        if v.get('status'):
                                            if v['status'] == 'start' or v['status'] == 'stop':
                                                insert_users_table(username=v['username'], userpass=v['userpass'], status=v['status'])
                                            else:
                                                print("\033[31;1m" + v['username'] + "指定了" + "未知的状态" + v['status'] + ", 请修改后重新添加!\033[0m")
                                                continue
                                        else:
                                            insert_users_table(username=v['username'], userpass=v['userpass'])
                                    userid = select_users_table(v['username'])
                                    print(v['username'] + '(userid:' + str(userid) + ')' + ' 添加成功!')
                                result=select_users_groups_table(userid,usrgrpid)
                                if result:
                                    print("\033[31;1muserid: " + str(userid) + "(username: " + v[
                                        'username'] + ")" + " 关联 " + "usrgrpid: " + str(usrgrpid) + "(usrgrpname: " + v[
                                              'usrgrpname'] + ")" + " 已存在于users_groups表, 无需添加!\033[0m")
                                    continue
                                else:
                                    insert_users_groups_table(userid,usrgrpid)
                                    print('userid: ' + str(userid) + '(username: ' + v['username'] + ')' +
                                      ' 关联 ' + 'usrgrpid: ' + str(usrgrpid) + '(usrgrpname: ' +
                                      v['usrgrpname'] + ')' + ' 成功!')
                            else:
                                print("\033[31;1m创建"+v['username']+"时 "+v['usrgrpname']+" 组不存在, 请先创建该组!\033[0m")
                                continue
                    else:
                        userid = select_users_table(v['username'])
                        if userid:
                            print("\033[31;1m"+v['username'] + "(userid:" + str(userid) + ")" + " 已存在于users表, 无需添加!\033[0m")
                            continue
                        else:
                            if v.get('role'):
                                if v['role'] == 'admin' or v['role'] == 'user':
                                    if v.get('status'):
                                        if v['status'] == 'start' or v['status'] == 'stop':
                                            insert_users_table(username=v['username'], userpass=v['userpass'],role=v['role'], status=v['status'])
                                        else:
                                            print("\033[31;1m" + v['username'] + "指定了" + "未知的状态" + v['status'] + ", 请修改后重新添加!\033[0m")
                                            continue
                                    else:
                                        insert_users_table(username=v['username'], userpass=v['userpass'], role=v['role'])
                                else:
                                    print("\033[31;1m" + v['username'] + "指定了" + "未知的角色" + v['role'] + ", 请修改后重新添加!\033[0m")
                                    continue
                            else:
                                if v.get('status'):
                                    if v['status'] == 'start' or v['status'] == 'stop':
                                        insert_users_table(username=v['username'], userpass=v['userpass'],status=v['status'])
                                    else:
                                        print("\033[31;1m" + v['username'] + "指定了" + "未知的状态" + v['status'] + ", 请修改后重新添加!\033[0m")
                                        continue
                                else:
                                    insert_users_table(username=v['username'], userpass=v['userpass'])
                            userid = select_users_table(v['username'])
                            print(v['username'] + '(userid:' + str(userid) + ')' + ' 添加成功!')

def create_usrgrp():
    file_path=BASE_DIR+"/conf/db_tables_yaml/usrgrp.yaml"
    with open(file_path,'r') as usrgrp_yaml_file:
        data=yaml.load(usrgrp_yaml_file, Loader=yaml.FullLoader)
    if data:
        for k,v in data.items():
            print('----------')
            if len(str(v['usrgrpname'])) > 20:
                print('用户组名长度不能大于20个字符, 请检查' + v['usrgrpname'] + '的长度!')
                continue
            else:
                usrgrpid=select_usrgrp_table(v['usrgrpname'])
                if usrgrpid:
                    print("\033[31;1m"+v['usrgrpname'] + "(usrgrpid:" + str(usrgrpid) + ")" + " 已存在于usrgrp表, 无需添加!\033[0m")
                    continue
                else:
                    insert_usrgrp_table(v['usrgrpname'])
                    usrgrpid = select_usrgrp_table(v['usrgrpname'])
                    print(v['usrgrpname'] + '(usrgrpid:' + str(usrgrpid) + ')' + ' 添加成功!')

def create_hosts():
    file_path=BASE_DIR+"/conf/db_tables_yaml/hosts.yaml"
    with open(file_path,'r') as hosts_yaml_file:
        data=yaml.load(hosts_yaml_file, Loader=yaml.FullLoader)
    if data:
        for k, v in data.items():
            print('----------')
            if v.get('hstgrpname'):
                hstgrpid = select_hstgrp_table(v['hstgrpname'])
                if hstgrpid:
                    hostid = select_hosts_table(v['hostip'])
                    if hostid:
                        print("\033[31;1m"+v['hostip'] + "(hostid:" + str(hostid) + ")" + " 已存在于hosts表, 无需添加!\033[0m")
                    else:
                        if v.get('hostport'):
                            insert_hosts_table(v['hostip'], v['hostport'])
                        else:
                            insert_hosts_table(v['hostip'])
                        hostid = select_hosts_table(v['hostip'])
                        print(v['hostip'] + '(hostid:' + str(hostid) + ')' + ' 添加成功!')
                    result = select_hosts_groups_table(hostid, hstgrpid)
                    if result:
                        print("\033[31;1mhostid: " + str(hostid) + "(hostip: " + v[
                            'hostip'] + ")" + " 关联 " + "hstgrpid: " + str(hstgrpid) + "(hstgrpname: " + v[
                                  'hstgrpname'] + ")" + " 已存在于hosts_groups表, 无需添加!\033[0m")
                        continue
                    else:
                        insert_hosts_groups_table(hostid, hstgrpid)
                        print('hostid: ' + str(hostid) + '(hostip: ' + v['hostip'] + ')' +
                              ' 关联 ' + 'hstgrpid: ' + str(hstgrpid) + '(hstgrpname: ' +
                              v['hstgrpname'] + ')' + ' 成功!')
                else:
                    print("\033[31;1m创建" + v['hostip'] + "时 " + v.get('hstgrpname') + " 组不存在, 请先创建该组!\033[0m")
                    continue
            else:
                hostid = select_hosts_table(v['hostip'])
                if hostid:
                    print("\033[31;1m"+v['hostip'] + "(hostid:" + str(hostid) + ")" + " 已存在于hosts表, 无需添加!\033[0m")
                    continue
                else:
                    if v.get('hostport'):
                        insert_hosts_table(v['hostip'], v['hostport'])
                    else:
                        insert_hosts_table(v['hostip'])
                    hostid = select_hosts_table(v['hostip'])
                    print(v['hostip'] + '(hostid:' + str(hostid) + ')' + ' 添加成功!')

def create_hstgrp():
    file_path=BASE_DIR+"/conf/db_tables_yaml/hstgrp.yaml"
    with open(file_path,'r') as hstgrp_yaml_file:
        data=yaml.load(hstgrp_yaml_file, Loader=yaml.FullLoader)
    if data:
        for k,v in data.items():
            print('----------')
            if len(str(v['hstgrpname'])) > 20:
                print('主机组名长度不能大于20个字符, 请检查' + v['hstgrpname'] + '的长度!')
                continue
            else:
                hstgrpid=select_hstgrp_table(v['hstgrpname'])
                if hstgrpid:
                    print("\033[31;1m"+v['hstgrpname'] + "(hstgrpid:" + str(hstgrpid) + ")" + " 已存在于hstgrp表, 无需添加!\033[0m")
                    continue
                else:
                    insert_hstgrp_table(v['hstgrpname'])
                    hstgrpid = select_hstgrp_table(v['hstgrpname'])
                    print(v['hstgrpname'] + '(hstgrpid:' + str(hstgrpid) + ')' + ' 添加成功!')

def create_remoteusers():
    file_path = BASE_DIR + "/conf/db_tables_yaml/remoteusers.yaml"
    with open(file_path, 'r') as remoteusers_yaml_file:
        data = yaml.load(remoteusers_yaml_file, Loader=yaml.FullLoader)
    if data:
        for k,v in data.items():
            print('----------')
            if len(str(v['remoteusername'])) > 20 or len(str(v['remoteuserpass'])) > 20:
                print('远程用户名和密码长度不能大于20个字符, 请检查' + v['remoteusername'] + '和' + v['remoteuserpass'] + '的长度!')
                continue
            else:
                remoteuserid=select_remoteusers_table(v['remoteusername'])
                if remoteuserid:
                    print("\033[31;1m"+v['remoteusername'] + "(remoteuserid:" + str(remoteuserid) + ")" + " 已存在于remoteusers表, 无需添加!\033[0m")
                else:
                    insert_remoteusers_table(v['remoteusername'],v['remoteuserpass'])
                    remoteuserid = select_remoteusers_table(v['remoteusername'])
                    print(v['remoteusername'] + '(remoteuserid:' + str(remoteuserid) + ')' + ' 添加成功!')

def create_authorization():
    file_path = BASE_DIR + "/conf/db_tables_yaml/authorization.yaml"
    with open(file_path, 'r') as authorization_yaml_file:
        data = yaml.load(authorization_yaml_file, Loader=yaml.FullLoader)
    if data:
        for k,v in data.items():
            print('----------')
            if len(str(v['authorizationname'])) > 30:
                print('策略名长度不能大于30个字符, 请检查' + v['authorizationname'] + '的长度!')
                continue
            else:
                result=select_authorization_table(v['authorizationname'])
                if result:
                    print("\033[31;1m"+v['authorizationname'] + " 已存在于authorization表, 请更换策略名称后再添加!\033[0m")
                    continue
                else:
                    remoteuserid = select_remoteusers_table(v['remoteusername'])
                    if remoteuserid:
                        if v.get('username') and v.get('usrgrpname'):
                            print("\033[31;1mERROR: username 和 usrgrpname同时只能设置一个\033[0m")
                            continue
                        if v.get('hostip') and v.get('hstgrpname'):
                            print("\033[31;1mERROR: hostip 和 hstgrpname同时只能设置一个\033[0m")
                            continue
                        if v.get('username'):
                            userid=select_users_table(v['username'])
                            if userid:
                                if v.get('hostip'):
                                    hostid = select_hosts_table(v['hostip'])
                                    if hostid:
                                        insert_authorization_table(v['authorizationname'],userid,None,hostid,None,remoteuserid)
                                        print(v['authorizationname'] + ' 授权策略添加成功!')
                                    else:
                                        print("\033[31;1m"+v['hostip'] + "主机不存在, 请先添加此主机\033[0m")
                                        continue
                                else:
                                    hstgrpid = select_hstgrp_table(v['hstgrpname'])
                                    if hstgrpid:
                                        insert_authorization_table(v['authorizationname'],userid,None,None,hstgrpid,remoteuserid)
                                        print(v['authorizationname'] + ' 授权策略添加成功!')
                                    else:
                                        print("\033[31;1m"+v['hstgrpname'] + "主机组不存在, 请先添加此主机组\033[0m")
                                        continue
                            else:
                                print("\033[31;1m"+v['username'] + "用户不存在, 请先添加此用户\033[0m")
                                continue
                        else:
                            usrgrpid = select_usrgrp_table(v['usrgrpname'])
                            if usrgrpid:
                                if v.get('hostip'):
                                    hostid = select_hosts_table(v['hostip'])
                                    if hostid:
                                        insert_authorization_table(v['authorizationname'],None,usrgrpid,hostid,None,remoteuserid)
                                        print(v['authorizationname'] + ' 授权策略添加成功!')
                                    else:
                                        print("\033[31;1m"+v['hostip'] + "主机不存在, 请先添加此主机\033[0m")
                                        continue
                                else:
                                    hstgrpid = select_hstgrp_table(v['hstgrpname'])
                                    if hstgrpid:
                                        insert_authorization_table(v['authorizationname'],None,usrgrpid,None,hstgrpid,remoteuserid)
                                        print(v['authorizationname'] + ' 授权策略添加成功!')
                                    else:
                                        print("\033[31;1m"+v['hstgrpname'] + "主机组不存在, 请先添加此主机组\033[0m")
                                        continue
                            else:
                                print("\033[31;1m"+v['usrgrpname'] + "用户组不存在, 请先添加此用户组\033[0m")
                                continue
                    else:
                        print("\033[31;1m"+v['remoteusername'] + "远程用户不存在, 请先添加此远程用户\033[0m")
                        continue