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

from .base import *  # NOQA

# # SECURITY安全设置 - 支持https时建议开启
# # Django以下的几个安全设置均依赖下面这个SecurityMiddleware中间件
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# # 将所有非SSL(http)请求永久重定向到SSL(https), 与Nginx的301重定向设置选其一即可
# SECURE_SSL_REDIRECT = True
# # 仅通过https传输cookie
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SECURE = True
# # 严格要求使用https协议传输
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# # HSTS为单位时间，单位秒
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_SECONDS = 60
# # 防止浏览器猜测资产的内容类型
# SECURE_CONTENT_TYPE_NOSNIFF = True

# 数据库配置
DATABASES = {
    'default': {
        # 如果使用MySQL数据库，会重新建一个test_项目名称_db的数据库，或者自己手动配置
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'DjangoAuth',
        'USER': 'root',
        'PASSWORD': 'WMU-sulab-2022',
        # 'PASSWORD': 'laobatai981218',
        'OPTIONS': {
            'charset': 'utf8mb4',
            # 'timezone': 'Asia/Shanghai',
            'timeout': 60,
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
        'PORT': '3306',
        'NAME': 'SilencerAtlas',
        'USER': 'root',
        'PASSWORD': 'WMU-sulab-2022',
        # 'PASSWORD': 'laobatai981218',
        'OPTIONS': {
            'charset': 'utf8mb4',
            # 'timezone': 'Asia/Shanghai',
            'timeout': 60,
        },
        # 'CONN_MAX_AGE': 36000,
        'TEST': {
            'NAME': 'SilencerAtlasTest'
        }
    }
}
