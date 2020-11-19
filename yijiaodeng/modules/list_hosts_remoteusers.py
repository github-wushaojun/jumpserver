#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

from conf import conn_db_setting
from modules import ssh_login

conn = conn_db_setting.engine.connect()

hosts_remoteusers_all = {}
hostips_hostports = {}
remoteusernames_remoteuserpass = {}
hostid_hostip_temp = {}
only_hostips = []
only_remoteusers = []

def main(my_name):
    break_flag = False

    # 清空主机列表，防止多次选择，列表数据重复
    only_hostips.clear()
    list_hosts(my_name)
    while True:
        try:
            input_str = input('请选择主机编号, 输入q返回主菜单, 回车显示主机列表: ').strip()
            if input_str.isdigit():
                if only_hostips[int(input_str)]:
                    # 清空用户列表，防止多次选择，列表数据重复
                    only_remoteusers.clear()
                    hostip_choice = only_hostips[int(input_str)]
                    list_remoteusers(int(input_str))
                    while True:
                        try:
                            input_str = input('请选择登录用户编号, 输入q返回主菜单: ').strip()
                            if input_str.isdigit():
                                if only_remoteusers[int(input_str)]:
                                    remoteusername_choice = only_remoteusers[int(input_str)]
                                    ssh_login.ssh_login(my_name, hostip_choice,hostips_hostports[hostip_choice],remoteusername_choice,remoteusernames_remoteuserpass[remoteusername_choice])
                                    break
                            elif input_str == 'q':
                                break_flag = True
                                break
                            elif input_str == "":
                                for index, remoteusername in enumerate(only_remoteusers):
                                    print([index], remoteusername)
                            else:
                                print('请输入用户编号!')
                                continue
                        except IndexError as e:
                            print('用户编号输入有误, 请重新输入!')
                            continue
            elif input_str == 'q':
                break
            elif input_str == '':
                for index, hostip in enumerate(only_hostips):
                    print([index], hostip)
            else:
                print('请输入主机编号!')
                continue
            if break_flag:
                break
        except IndexError as e:
            print('主机编号输入有误, 请重新输入!')
            continue

def list_hosts(my_name):
    # 查找用户所包含的资产
    user_to_hostid_cursor = conn.execute(
        "select hostid,remoteuserid from authorization where userid in (select userid from users where username=%(username)s) and hostid is not null;",
        username=my_name
    )
    user_to_hostid_result = user_to_hostid_cursor.fetchall()
    if user_to_hostid_result:
        for hostid, remoteuserid in user_to_hostid_result:
            hosts_remoteusers_all.setdefault(hostid, []).append(remoteuserid)

    # 查找用户所包含的所有资产组
    user_to_hstgrpid_cursor = conn.execute(
        "select hstgrpid,remoteuserid from authorization where userid in (select userid from users where username=%(username)s) and hstgrpid is not null;",
        username=my_name
    )
    user_to_hstgrpid_result = user_to_hstgrpid_cursor.fetchall()
    if user_to_hstgrpid_result:
        for hstgrpid, remoteuserid in user_to_hstgrpid_result:
            # 通过查找到的资产组查找包含的所有资产
            user_to_hstgrpid_to_hostid_cursor = conn.execute(
                "select hostid from hosts_groups where hstgrpid=%(hstgrpid)s;", hstgrpid=hstgrpid
            )
            user_to_hstgrpid_to_hostid_result = user_to_hstgrpid_to_hostid_cursor.fetchall()
            if user_to_hstgrpid_to_hostid_result:
                for hostid, in user_to_hstgrpid_to_hostid_result:
                    hosts_remoteusers_all.setdefault(hostid, []).append(remoteuserid)

    # 查找用户所对应的用户组所包含的资产
    usrgrp_to_hostid_cursor = conn.execute(
        "select hostid,remoteuserid from authorization where usrgrpid in (select usrgrpid from users_groups where userid in (select userid from users where username=%(username)s)) and hostid is not null;",
        username=my_name
    )
    usrgrp_to_hostid_cursor_result = usrgrp_to_hostid_cursor.fetchall()
    if usrgrp_to_hostid_cursor_result:
        for hostid, remoteuserid in usrgrp_to_hostid_cursor_result:
            hosts_remoteusers_all.setdefault(hostid, []).append(remoteuserid)

    # 查找用户所对应的用户组所包含的所有资产组
    usrgrp_to_hstgrpid_cursor = conn.execute(
        "select hstgrpid,remoteuserid from authorization where usrgrpid in (select usrgrpid from users_groups where userid in (select userid from users where username=%(username)s)) and hstgrpid is not null;",
        username=my_name
    )
    usrgrp_to_hstgrpid_result = usrgrp_to_hstgrpid_cursor.fetchall()
    if usrgrp_to_hstgrpid_result:
        for hstgrpid, remoteuserid in usrgrp_to_hstgrpid_result:
            # 通过查找到的资产组查找包含的所有资产
            user_to_hstgrpid_to_hostid_cursor = conn.execute(
                "select hostid from hosts_groups where hstgrpid=%(hstgrpid)s;", hstgrpid=hstgrpid
            )
            user_to_hstgrpid_to_hostid_result = user_to_hstgrpid_to_hostid_cursor.fetchall()
            if user_to_hstgrpid_to_hostid_result:
                for hostid, in user_to_hstgrpid_to_hostid_result:
                    hosts_remoteusers_all.setdefault(hostid, []).append(remoteuserid)
        # print(hosts_remoteusers_all)

    for hostid in hosts_remoteusers_all.keys():
        hostid_to_hostip = conn.execute(
            "select hostid,hostip,hostport from hosts where hostid=%(hostid)s;", hostid=hostid
        )
        for hostid, hostip, hostport in hostid_to_hostip:
            hostips_hostports[hostip] = hostport
            hostid_hostip_temp[hostip] = hostid
            only_hostips.append(hostip)

    # print(only_hostips)
    for index, hostip in enumerate(only_hostips):
        print([index], hostip)

def list_remoteusers(input_str):
    for remoteuserid in list(set(hosts_remoteusers_all[hostid_hostip_temp[only_hostips[input_str]]])):
        remoteuserid_to_remoteusername = conn.execute(
            "select remoteuserid,remoteusername,remoteuserpass from remoteusers where remoteuserid=%(remoteuserid)s;",
            remoteuserid=remoteuserid
        )
        for remoteuserid, remoteusername, remoteuserpass in remoteuserid_to_remoteusername:
            remoteusernames_remoteuserpass[remoteusername] = remoteuserpass
            only_remoteusers.append(remoteusername)

    # print(only_remoteusers)
    for index, remoteusername in enumerate(only_remoteusers):
        print([index], remoteusername)

if __name__ == '__main__':
    list_hosts('wsj')