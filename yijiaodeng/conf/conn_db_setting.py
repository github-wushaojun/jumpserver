#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey, Enum, UniqueConstraint

# 连接数据库
engine = create_engine("mysql+pymysql://root:12345678@127.0.0.1:3306/yijiaodeng?charset=utf8", encoding='utf-8', echo=False)

# 获取元数据
metadata = MetaData()

# 定义用户表和用户组表以及关联表
users = Table('users', metadata,
        Column('userid', Integer, primary_key=True),
        Column('username', String(20), nullable=False),
        Column('userpass', String(32), nullable=False),
        Column('role', Enum('admin','user'), nullable=False, server_default='user'),
        Column('status', Enum('start','stop'), nullable=False, server_default='start'),
        UniqueConstraint('username')
    )

usrgrp = Table('usrgrp', metadata,
        Column('usrgrpid', Integer, primary_key=True),
        Column('usrgrpname', String(20), nullable=False),
        UniqueConstraint('usrgrpname')
    )

users_groups = Table('users_groups', metadata,
        Column('id', Integer, primary_key=True),
        Column('userid', Integer, ForeignKey('users.userid'), nullable=False),
        Column('usrgrpid', Integer, ForeignKey('usrgrp.usrgrpid'), nullable=False),
        UniqueConstraint('userid','usrgrpid')
    )


# 定义资产表和资产组表以及关联表
hosts = Table('hosts', metadata,
        Column('hostid', Integer, primary_key=True),
        Column('hostip', String(20), nullable=False),
        Column('hostport', Integer, nullable=False, server_default='22'),
        UniqueConstraint('hostip','hostport')
    )

hstgrp = Table('hstgrp', metadata,
        Column('hstgrpid', Integer, primary_key=True),
        Column('hstgrpname', String(20), nullable=False),
        UniqueConstraint('hstgrpname')
    )

hosts_groups = Table('hosts_groups', metadata,
        Column('id', Integer, primary_key=True),
        Column('hostid', Integer, ForeignKey('hosts.hostid'), nullable=False),
        Column('hstgrpid', Integer, ForeignKey('hstgrp.hstgrpid'), nullable=False),
        UniqueConstraint('hostid','hstgrpid')
    )

# 定义远程用户表
remoteusers = Table('remoteusers', metadata,
        Column('remoteuserid', Integer, primary_key=True),
        Column('remoteusername', String(20), nullable=False),
        Column('remoteuserpass', String(20), nullable=False),
        UniqueConstraint('remoteusername')
    )

# 定义授权表
authorization = Table('authorization', metadata,
        Column('id', Integer, primary_key=True),
        Column('authorizationname', String(30), nullable=False),
        Column('userid', Integer),
        Column('usrgrpid', Integer),
        Column('hostid', Integer),
        Column('hstgrpid', Integer),
        Column('remoteuserid', Integer, nullable=False),
        UniqueConstraint('authorizationname')
    )

# 定义审计日志表
auditlog = Table('auditlog', metadata,
        Column('id', Integer, primary_key=True),
        Column('time', DateTime, nullable=False),
        Column('username', String(20), nullable=False),
        Column('hostip', String(20), nullable=False),
        Column('remoteusername', String(20), nullable=False),
        Column('content', String(60), nullable=True)
    )

if __name__ == "__main__":
        import os, sys
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(BASE_DIR)
        from modules.method import pass_md5_calculate

        # 创建数据表，如果数据表存在，则忽视
        metadata.create_all(engine)
        conn = engine.connect()
        conn.execute(
        "insert into users(username,userpass,role,status)values(%(username)s,%(userpass)s,%(role)s,%(status)s)",username='admin', userpass=pass_md5_calculate(b'admin'), role='admin', status='start'
        )

