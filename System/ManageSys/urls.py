"""ManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

admin.site.site_title = '用户权限管理'
admin.site.site_header = '用户权限管理'

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # 注意，不是末尾函数(如include)最后都要加上'/'，但空字符千万也别加'/'
]
