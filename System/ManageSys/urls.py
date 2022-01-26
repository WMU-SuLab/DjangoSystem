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
from django.contrib.auth import views as auth_views
from django.urls import path, include
# 导入server服务
# from django.views.static import serve

# from ManageSys.settings.base import STATIC_ROOT

admin.site.site_title = '用户权限管理'
admin.site.site_header = '用户权限管理'

urlpatterns = [
    # 注意，不是末尾函数(如include)最后都要加上'/'，但空字符千万也别加'/'
    path('silencer_atlas/', include('SilencerAtlas.views', namespace='SilencerAtlas')),
    # 用户权限管理
    path('admin/', admin.site.urls, name='admin'),
    # 增加密码重置功能
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset', ),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done', ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm', ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete', ),
    # 自己提供静态资源服务，生产环境，static静态文件代理
    # path('/static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]
