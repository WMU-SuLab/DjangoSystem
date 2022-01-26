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

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 如果使用MySQL数据库，会重新建一个test_项目名称_db的数据库，或者自己手动配置
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'Auth',
        'USER': 'root',
        # 'PASSWORD': 'wmu-sulab',
        'PASSWORD': 'laobatai981218',
        'OPTIONS': {
            'charset': 'utf8mb4'
        },
        'TEST': {
            'NAME': 'AuthTest'
        }
    },
    'SilencerAtlas': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'SilencerAtlas',
        'USER': 'root',
        # 'PASSWORD': 'wmu-sulab',
        'PASSWORD': 'laobatai981218',
        'OPTIONS': {
            'charset': 'utf8mb4'
        },
        'TEST': {
            'NAME': 'SilencerAtlasTest'
        }
    }
}
