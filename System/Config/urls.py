from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, reverse
from django.urls import path, include

# 导入server服务
# from django.views.static import serve

# from Manage.settings.base import STATIC_ROOT

admin.site.site_title = '用户权限管理'
admin.site.site_header = '用户权限管理'


# 首页重定向
def index_redirect(request):
    return redirect(reverse('SilencerAtlas:page:index'))


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
    path('', index_redirect, name='index'),
]
