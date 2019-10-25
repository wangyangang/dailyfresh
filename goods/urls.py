from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    re_path(r'^detail/(\d+)', views.DetailView.as_view(), name='detail'),
    re_path(r'^list/(?P<type_id>\d+)/(?P<page>\d+)', views.ListView.as_view(), name='list'),
    re_path(r'^query/', views.QueryView.as_view(), name='query'),
]