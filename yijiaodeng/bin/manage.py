#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "wushaojun"

import os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    from modules import jumpserver_login
    jumpserver_login.login()