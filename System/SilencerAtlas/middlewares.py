# -*- encoding: utf-8 -*-
"""
@File Name      :   middlewares.py    
@Create Time    :   2021/10/17 15:57
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

import json
import time

from django.http import HttpResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class NewMiddlewareMixin(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request, *args, **kwargs):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class TimeItMiddleware(MiddlewareMixin):
    # 这是请求来到middleware的时候进入的第一个方法
    # 一般可以在这里做一些校验，如用户登录、请求头、验证头校验
    # 返回值类型只有HttpResponse或者None
    # 如果返回值是HttpResponse，接下来只会执行process_response，其他方法会被跳过，不执行
    # 如果这个middleware是settings.py中配置的第一个，接下来的middleware也会被跳过
    # 如果返回None，就会继续执行其他方法
    def process_request(self, request):
        self.start_time = time.time()

        return

    # 在process_request方法之后执行
    # 返回值同process_request，如果返回值是None，会自动执行view函数，从而得到最终的response
    def process_view(self, request, func, *args, **kwargs):
        """
        :func:即view函数
        """
        if request.path != reverse('index'):
            return None
        start = time.time()
        response = func(request)
        cost = time.time() - start
        print('process view cost: {:.2f}s'.format(cost))
        return response

    # 发生异常的时候会进入这个方法，如view函数执行错误，或者渲染模板出错
    # 但是如果在前面的process_view方法中手动调用了func，即使发生异常也不会触发到这个函数
    # 如果返回None就是不处理，这种情况下Django会使用自己的异常模板
    def process_exception(self, request, exception):
        pass

    # 如果是使用了模板的response，就会来到这个方法
    # 一般在这个方法中会修改返回头
    def process_template_response(self, request, response):
        return response

    # 所有流程处理完之后来到这个方法
    def process_response(self, request, response):
        cost = time.time() - self.start_time
        print('request to response cost: {:.2f}s'.format(cost))
        return response


class JSONMiddleware(MiddlewareMixin):
    """
    Process application/json requests data from GET and POST requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)


    def __call__(self, request):
        if 'application/json' in request.META.get('CONTENT_TYPE'):
            try:
                data = json.loads(request.body.decode('utf-8'))
                request.json = data
            except json.JSONDecodeError:
                return HttpResponse("JSON Decode Error", status=400)
        else:
            request.json=None
        return self.get_response(request)
