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
from zoneinfo import ZoneInfo

from . import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-k7t++81e%dpa!a^#2$7equ8+-=pu+52jf9x8bro#k2-k8!2n3e')
HASHID_FIELD_SALT = os.environ.get('HASHID_FIELD_SALT', 'wmu su-lab hashids salt secret key')
ALLOWED_HOSTS = ['*']

# Application definition
# 加载顺序是从上往下
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_mysql',
    'simpleui',
    "corsheaders",
    'rest_framework',
    'drf_spectacular',
    'Common',
    'SilencerAtlas',
]

DATABASE_APPS_MAPPING = {
    # example:'app_name':'database_name',
    'admin': 'default',
    'auth': 'default',
    'contenttypes': 'default',
    'sessions': 'default',
    'Common':'default',
    'SilencerAtlas': 'SilencerAtlas',
}

# 如果缓存使用数据库，则指定缓存表存放到的数据库
CACHE_DATABASE = 'default'

DATABASE_ROUTERS = [
    # 使用多个数据库缓存表作为缓存时候需要添加的路由，需要放在一般的路由之前
    # 'Config.router.CacheRouter',
    'Config.router.DatabaseRouter',
]

MIDDLEWARE = [
    # 'Common.utils.middlewares.TimeItMiddleware',
    'Common.utils.middlewares.JSONMiddleware',
    # CACHE MIDDLEWARE 顺序：https://docs.djangoproject.com/zh-hans/4.0/topics/cache/#the-per-site-cache
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 缓存整个站点
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

# 自定义项目入口url是哪个文件
ROOT_URLCONF = 'Config.urls'

# 哪个引擎放前面就默认使用哪个
# 建议只配置django引擎，如果非要使用jinja2语法，还是得有django引擎，否则admin会失效
# 而使用内置的jinja2引擎即使做了environment更改，语法还是和django的不一样
# 如果项目使用了两种模板引擎，需要配置两个templates文件夹以区分
# 注意：django渲染引擎的语法和原生的jinja2不一样
TEMPLATES = [
    # 配置jinja2引擎
    # {
    #     'NAME': 'jinja2',
    #     'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #     'DIRS': [
    #         os.path.join(BASE_DIR, 'templates_jinja2'),
    #         os.path.join(BASE_DIR, 'SilencerAtlas', 'templates_jinja2'),
    #     ],
    #     'APP_DIRS': True,
    #     'OPTIONS': {
    #         # 手动加载自己定义的jinja2环境
    #         "environment": 'utils.jinja2_env.environment',
    #         # 為了避免 XSS 攻擊
    #         'autoescape': True,
    #         'context_processors': [
    #             'django.template.context_processors.i18n',
    #             'django.template.context_processors.media',
    #             'django.template.context_processors.static',
    #             'django.template.context_processors.tz',
    #             'django.template.context_processors.debug',
    #             'django.template.context_processors.request',
    #             'django.contrib.auth.context_processors.auth',
    #             'django.contrib.messages.context_processors.messages',
    #         ],
    #     },
    # },
    # 通过django_jinja配置jinja2模板引擎
    #     {
    #         "BACKEND": "django_jinja.backend.Jinja2",
    #         "DIRS": [
    #             os.path.join(BASE_DIR, 'templates'),
    #             os.path.join(BASE_DIR, 'SilencerAtlas', 'templates'),
    #         ],
    #         "APP_DIRS": True,
    #         "OPTIONS": {
    #             # "match_extension": ".html",
    #             # "match_extension": ".jinja",
    #             'context_processors': [
    #                 'django.template.context_processors.i18n',
    #                 'django.template.context_processors.media',
    #                 'django.template.context_processors.static',
    #                 'django.template.context_processors.tz',
    #                 'django.template.context_processors.debug',
    #                 'django.template.context_processors.request',
    #                 'django.contrib.auth.context_processors.auth',
    #                 'django.contrib.messages.context_processors.messages',
    #             ],
    #         }
    #     },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 定义了一个目录列表，模板引擎按列表顺序搜索这些目录以查找模板源文件。
        'DIRS': [
            os.path.join(BASE_DIR, 'Common', 'templates'),
            os.path.join(BASE_DIR, 'SilencerAtlas', 'templates'),
        ],
        # 告诉模板引擎是否应该进入每个已安装的应用中查找模板。通常请将该选项保持为True。
        # 所以首先会到配置模板路径下找模板文件，之后会到 INSTALLED_APPS 中每个应用下面的templates文件夹中找模板文件
        # 最好在app下面的模板文件夹需要和static一样，添加app名称的文件夹
        'APP_DIRS': True,
        'OPTIONS': {
            # autoescape：一个布尔值，用于控制是否启用HTML自动转义功能。默认为True。
            # context_processors: 以"."为分隔符的Python调用路径的列表。默认是个空列表。
            # debug：打开/关闭模板调试模式的布尔值。默认和setting中的DEBUG有相同的值。
            # loaders'：模板加载器类的虚拟Python路径列表。默认值取决于DIRS和APP_DIRS的值。
            # string_if_invalid：非法变量时输出的字符串。默认为空字符串。
            # file_charset：用于读取磁盘上的模板文件的字符集编码。默认为FILE_CHARSET的值。
            # libraries：用于注册模板引擎。 这可以用于添加新的库或为现有库添加备用标签。
            # builtins：以圆点分隔的Python路径的列表。 每个元素都是一个py文件，文件中编写模板标签和过滤器。这些tag和filter会成为内置的类型，无需通过{% load %}加载即可开箱使用。
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
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

WSGI_APPLICATION = 'Config.wsgi.application'

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

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
TZ_INFO = ZoneInfo(TIME_ZONE)

USE_TZ = True

USE_I18N = True
# 数据和时间格式
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# 静态文件配置
# Django提供了collectstatic命令，用来收集所有的静态文件到STATIC_ROOT配置的目录中，这样就可以使用Nginx这样的软件来配置静态资源路径了
# 默认情况是在 STATICFILES_DIRS 中定义的所有位置(更优先)和 INSTALLED_APPS 配置指定的应用程序的 'static' 目录中查找
STATIC_ROOT = os.path.join(BASE_DIR, 'Common', 'static')
# 引用位于 STATIC_ROOT 中的静态文件时要使用的 URL。
STATIC_URL = '/static/'
# 用于指定的静态资源所在的目录
# 由于多个同名文件会产生混淆，所以需要在app的static文件夹下面再建一个与app同名的文件夹，而所有公用的文件则不需要添加前缀
# 如果出现了STATICFILES_DIRS包含STATIC_ROOT，在逻辑上就出现了我把自己打包到自己里面，这是行不通的。
# STATICFILES_DIRS配置的是不在应用下static文件夹内的静态资源的文件夹，所以如果是放在static下的，就不用配置，否则会重复，报错：found another file with the destination path
STATICFILES_DIRS = [
    # 公共静态资源
    # 不知道为什么pycharm非得不加BASE_DIR才能在模板中提示静态资源路径，神奇的是django竟然不加BASE_DIR也能识别出来正确的路径，目前不清楚原理
    'Common/static_dev',
    # Django3.2使用Path模块后支持的写法
    # BASE_DIR / 'Common/static_dev',
    # 老版写法
    # os.path.join(BASE_DIR, 'Common', 'static'),
    # SilencerAtlas静态资源
    # 'SilencerAtlas/static',
    # BASE_DIR / 'SilencerAtlas/static'
    # os.path.join(BASE_DIR, 'SilencerAtlas', 'static'),
]

# 媒体文件配置
MEDIA_ROOT = os.path.join(BASE_DIR, 'Common', 'media')
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
# 默认主键配置
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 跨域相关设置
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

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# 邮件配置
# 管理员邮箱配置
ADMINS = (
    ('diklios', '1061995104@qq.com'),
)

MANAGERS = (
    ('sujz', 'sujz@wiucas.ac.cn'),
    ('yuanj', 'danielwyuan@gmail.com'),
    ('fandd', 'biofandd@gmail.com'),
)
# 发送邮件的后端
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 邮件smtp服务地址
EMAIL_HOST = 'smtp.126.com'
# EMAIL_HOST = "smtp.163.com"
# EMAIL_HOST = 'smtp.qq.com'
# SMTP端口号
# 默认是25，当其他端口号Connection unexpectedly closed的时候不妨试试默认的
# EMAIL_PORT = 25
# 服务器默认不能使用25端口，需要根据使用的邮件服务商情况改为别的端口
# EMAIL_USE_SSL和EMAIL_USE_TLS是互斥的，即只能有一个为True。
EMAIL_PORT = 465
# 是否启动SSL链接(安全链接)，默认False，它通常在 465 端口使用
EMAIL_USE_SSL = True
# EMAIL_PORT = 587
# 与SMTP服务器通信时，是否启动TLS链接(安全链接)，默认False，这用于显式 TLS 连接，一般在 587 端口
# EMAIL_USE_TLS = True
# ssl_certfile
EMAIL_SSL_CERTFILE = None
# ssl_keyfile
EMAIL_SSL_KEYFILE = None
# 超时，单位：s（秒）
# EMAIL_TIMEOUT= None
EMAIL_TIMEOUT = 20
# 是否以当地时区（True）或UTC（False）发送SMTP Date 邮件头
EMAIL_USE_LOCALTIME = True
# 邮箱登录用户名
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
# 邮箱登录密码
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
# 邮件标题前缀，默认是'[django]'
EMAIL_SUBJECT_PREFIX = '[WMU-IBBD]'
# 错误信息来自的电子邮件地址，例如发送到 ADMINS 和 MANAGERS 的邮件，这个地址只用于错误信息，它不是用 send_mail() 发送普通邮件的地址
SERVER_EMAIL = EMAIL_HOST_USER
# 邮件发送人地址，默认电子邮件地址，用于网站管理员的各种自动通信
# fred @ example.com 和 Fred < fred @ example.com > 形式都是合法的
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

