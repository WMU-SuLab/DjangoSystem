# -*- encoding: utf-8 -*-
"""
@File Name      :   gunicorn.py    
@Create Time    :   2022/1/26 17:14
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

import multiprocessing
import os

from Config.settings import BASE_DIR

# 绑定ip和端口号
bind = '0.0.0.0:5000'
# 监听队列
backlog = 512
# gunicorn要切换到的目的工作目录
chdir = str(BASE_DIR)
# 超时
timeout = 30
# 设置守护进程(linux有效)，请注意使用sunpervisor的时候不能后台运行
# daemon = 'true'
# 使用gevent模式，还可以使用sync 模式，默认的是sync模式
worker_class = 'gevent'
# 进程数
workers = multiprocessing.cpu_count() * 2 + 1
# 指定每个进程开启的线程数
threads = 3
# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = 'info'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 访问日志文件
accesslog = os.path.join(BASE_DIR, 'Common', 'logs', 'gunicorn', "access.log")
# 错误日志文件
errorlog = os.path.join(BASE_DIR, 'Common', 'logs', 'gunicorn', "error.log")
