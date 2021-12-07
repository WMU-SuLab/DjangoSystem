# -*- encoding: utf-8 -*-
"""
@File Name      :   base.py    
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

import os

from . import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k7t++81e%dpa!a^#2$7equ8+-=pu+52jf9x8bro#k2-k8!2n3e'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # 'SilencerAtlasPage.middlewares.TimeItMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ManagementSystem.urls'

# 哪个引擎放前面就使用哪个，暂时没研究明白怎么两个同时生效
# 注意：django渲染引擎的语法和原生的jinja2不一样
TEMPLATES = [
    # {
    #     'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #     # 首先会到配置模板路径下找模板文件，之后会到 INSTALLED_APPS 中每个应用下面的templates文件夹中找模板文件，所以在app下面的模板文件夹需要和static一样，添加app名称的文件夹
    #     'DIRS': [
    #         os.path.join(BASE_DIR, 'templates'),
    #         os.path.join(BASE_DIR, 'SilencerAtlasPage', 'templates'),
    #     ],
    #     'APP_DIRS': True,
    #     'OPTIONS': {
    #         'context_processors': [
    #             'django.template.context_processors.debug',
    #             'django.template.context_processors.request',
    #             'django.contrib.auth.context_processors.auth',
    #             'django.contrib.messages.context_processors.messages',
    #         ],
    #     },
    # },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 首先会到配置模板路径下找模板文件，之后会到 INSTALLED_APPS 中每个应用下面的templates文件夹中找模板文件，所以在app下面的模板文件夹需要和static一样，添加app名称的文件夹
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            # os.path.join(BASE_DIR, 'SilencerAtlasPage', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 这样以后在模版中就可以直接使用static标签，而不用手动的load了
            'builtins': ['django.templatetags.static'],
        },
    },
]

WSGI_APPLICATION = 'ManagementSystem.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# 设置语言
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'
# 设置时区
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
# 启用国际化语言
USE_I18N = True
# 数据和时间格式
USE_L10N = True
# 启用时区
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Django提供了collectstatic命令，用来收集所有的静态文件到STATIC_ROOT配置的目录中，这样就可以使用Nginx这样的软件来配置静态资源路径了
# 默认情况是在 STATICFILES_DIRS 中定义的所有位置(更优先)和 INSTALLED_APPS 配置指定的应用程序的 'static' 目录中查找
STATIC_ROOT = '/tmp/static'
# 引用位于 STATIC_ROOT 中的静态文件时要使用的 URL。
STATIC_URL = '/static/'
# 用于指定的静态资源所在的目录
# 由于多个同名文件会产生混淆，所以需要在app的static文件夹下面再建一个与app同名的文件夹，而所有公用的文件则不需要添加前缀
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'SilencerAtlasPage/static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 允许所有人访问
CORS_ORIGIN_ALLOW_ALL = True
# 或者指定白名单
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000',
    'http://localhost:8000',
)
# 指明在跨域访问中，后端是否支持对cookie的操作
CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

# CORS_ALLOW_HEADERS = (
#     'XMLHttpRequest',
#     'X_FILENAME',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
#     'Pragma',
# )
