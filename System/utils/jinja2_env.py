# -*- encoding: utf-8 -*-
"""
@File Name      :   jinja2_env.py    
@Create Time    :   2022/1/6 9:00
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def environment(**opts):
    """
    定义了static和url方法功能
    static获取文件前缀， 实现了在模板中简化路径编写
    将url和reverse方法绑定，可通过url方法在模板中完成重定向
    :param opts:
    :return:
    """
    env = Environment(**opts)
    env.globals.update({
        # 获取静态文件前缀
        # 注意这里即使更改了，使用的时候是{{static('')}}，而不是原来django的{%static ''%}
        "static": staticfiles_storage.url,
        "url": reverse  # 反向解析
    })
    return env
