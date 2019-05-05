# -*- coding: utf-8 -*-

import logging
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

########################## db ##########################
DB_NAME = "flerken"
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"

# sso db
# SSO_DB_NAME = "sso"
# SSO_DB_USER = "root"
# SSO_DB_PASSWORD = "root"
# SSO_DB_HOST = "127.0.0.1"
# SSO_DB_PORT = "3306"

########################## db ##########################


REDIS = {
    "HOST": "127.0.0.1",
    "PORT": 6379,
    "PASSWORD": ''
}

# 系统名称和子系统名称对应
SYSTEM_NAME = 'flerken'

# 日志目录
LOG = '/var/log/flerken'
logger = logging.getLogger('flerken')

DEBUG = True
