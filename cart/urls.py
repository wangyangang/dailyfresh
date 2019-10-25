from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.CartInfoView.as_view(), name='show'),
    re_path(r'add', views.CartAddView.as_view(), name='add'),  # 购物车添加记录
    re_path(r'update', views.CartUpdateView.as_view(), name='update'),
]