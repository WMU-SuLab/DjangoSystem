# -*- encoding: utf-8 -*-
"""
@File Name      :   develop.py    
@Create Time    :   2021/10/17 15:55
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
@other information
"""
__auth__ = 'diklios'

from .project import *  # NOQA

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # },
        # 只显示数据库查询语句
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
    },
}

# 设置数据库
DATABASES = {
    'default': {
        # 这个数据库是默认的sqlite数据库，测试用的数据库默认是存放于内存中
        'ENGINE': 'django.db.backends.sqlite3',
        # 测试环境的时候保持长连接
        'CONN_MAX_AGE': None,
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'django_auth.sqlite3'),
        'OPTIONS': {
            'timeout': 60,
        },
    },
    'SilencerAtlas': {
        'ENGINE': 'django.db.backends.sqlite3',
        'CONN_MAX_AGE': None,
        'NAME': os.path.join(BASE_DIR, 'silencer_atlas.sqlite3'),
        'OPTIONS': {
            'timeout': 60,
        },
    },
}

# 缓存
CACHES = {
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     'LOCATION': 'default_cache_table',
    # },
    # 'SilencerAtlas': {
    #     'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     'LOCATION': 'silencer_atlas_cache_table',
    # }
    'default': {
        # 使用memcached
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        # 使用存在的进程
        # 'LOCATION': 'unix:/tmp/memcached.sock',
        # 多台机器
        # 'LOCATION': [
        #     '172.19.26.240:11211',
        #     '172.19.26.242:11211',
        # ]
        'TIMEOUT': 60 * 10,
        'KEY_FUNCTION': lambda key, prefix_key, version: "django—system:%s" % key
    },
    # 'SilencerAtlas': {
    #     # 使用redis，django4.0之后支持redis
    #     'BACKEND': 'django.core.cache.backends.redis.RedisCache',
    #     'LOCATION': 'redis://127.0.0.1:6379',
    #     # 带身份验证的地址
    #     # 'LOCATION': 'redis://username:password@127.0.0.1:6379',
    #     # 多台机器
    #     # 'LOCATION': [
    #     #     'redis://127.0.0.1:6379', # leader
    #     #     'redis://127.0.0.1:6378', # read-replica 1
    #     #     'redis://127.0.0.1:6377', # read-replica 2
    #     # ],
    #     'TIMEOUT': 60 * 10,
    #     'KEY_FUNCTION': lambda key, prefix_key, version: "django:%s" % key
    # }
}


MANAGERS = (
    ('diklios', '1061995104@qq.com'),
)