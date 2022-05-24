# -*- encoding: utf-8 -*-
"""
@File Name      :   product.py    
@Create Time    :   2021/10/17 15:56
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

from .project import *

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s  %(asctime)s  %(module)s  %(funcName)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        # 如果使用supervisor可以不用配置file，supervisor的会将控制台的内容输出到日志
        # 'file':{
        #     'level':'INFO',
        #     'class':'logging.handlers.RotatingFileHandler',
        #     'filename':os.path.join(BASE_DIR,'logs','system.log'),
        #     'formatter': 'default',
        #     'maxBytes':1024*1024,
        #     'backupCount':5,
        # },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# 数据库配置
DATABASES = {
    'default': {
        # 如果使用MySQL数据库，会重新建一个test_项目名称_db的数据库，或者自己手动配置
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        # 'PORT': '3306',
        'PORT': '33060',
        'NAME': 'DjangoAuth',
        'USER': 'root',
        'PASSWORD': os.environ.get('DATABASE_DEFAULT_PASSWORD', ''),
        'OPTIONS': {
            # 'init_command': 'SET default_storage_engine=INNODB;',
            'charset': 'utf8mb4',
            # 'timezone': 'Asia/Shanghai',
            # 'timeout': 60,
        },
        # gevent和多线程的时候不要用
        # 'CONN_MAX_AGE': 36000,
        'TEST': {
            'NAME': 'DjangoAuthTest'
        }
    },
    'SilencerAtlas': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        # 'PORT': '3306',
        'PORT': '33060',
        'NAME': 'SilencerAtlas',
        'USER': 'root',
        'PASSWORD': os.environ.get('DATABASE_SILENCER_ATLAS_PASSWORD', ''),
        'OPTIONS': {
            # 'init_command': 'SET default_storage_engine=INNODB;',
            'charset': 'utf8mb4',
            # 'timezone': 'Asia/Shanghai',
            # 'timeout': 60,
        },
        # 'CONN_MAX_AGE': 36000,
        'TEST': {
            'NAME': 'SilencerAtlasTest'
        }
    },
}

# 缓存配置
CACHES = {
    'default': {
        # 使用memcached
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60 * 10,
        'KEY_FUNCTION': lambda key, prefix_key, version: "django—system:%s" % key
    },
}


# SECURITY安全设置 - 支持https时建议开启
# Django以下的几个安全设置均依赖 'django.middleware.security.SecurityMiddleware' 中间件，请注意是否在 MIDDLEWARE 中添加
# 和代理服务器配合，保证这是安全的HTTPS连接
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# 将所有非SSL(http)请求永久重定向到SSL(https), 与Nginx的301重定向设置选其一即可
SECURE_SSL_REDIRECT = True
# 如果一个 URL 路径与这个列表中的正则表达式相匹配，那么请求将不会被重定向到 HTTPS
# SECURE_REDIRECT_EXEMPT = []
# 仅通过https传输cookie
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
# 避免不甚用 HTTP 传输 CSRF cookie
CSRF_COOKIE_SECURE = True
# 严格要求使用https协议传输，SecurityMiddleware 在 HTTP 严格传输安全 头中添加 includeSubDomains 指令。除非 SECURE_HSTS_SECONDS 被设置为非零值，否则它没有任何效果。
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SecurityMiddleware 在 HTTP 严格传输安全头中添加 preload 指令。除非 SECURE_HSTS_SECONDS 设置为非零值，否则没有效果
SECURE_HSTS_PRELOAD = True
# HSTS为单位时间，单位秒
SECURE_HSTS_SECONDS = 60
# 防止浏览器猜测资产的内容类型
SECURE_CONTENT_TYPE_NOSNIFF = True
