from django.urls import re_path, path
from . import views


urlpatterns = [
    re_path(r'^place$', views.OrderPlaceView.as_view(), name='place'), # 提交订单页面显示
    re_path(r'^commit$', views.OrderCommitView.as_view(), name='commit'), # 订单创建
    re_path(r'^delete/$', views.OrderDeleteView.as_view(), name='delete'),
    re_path(r'^pay/$', views.OrderPayView.as_view(), name='pay'),
    re_path(r'^check/$', views.CheckPayView.as_view(), name='check'),
    re_path(r'^comment/(?P<order_id>.+)$', views.CommentView.as_view(), name='comment'),
]