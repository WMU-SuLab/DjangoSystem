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


from .base import *  # NOQA

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 这个数据库是默认的sqlite数据库，测试用的数据库默认是存放于内存中
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
