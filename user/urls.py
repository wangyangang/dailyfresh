from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^register/', views.RegisterView.as_view(), name='register'),
    re_path(r'^unverified-email/', views.UnverifiedEmail.as_view(), name='unverified-email'),
    re_path(r'^active/(.*)/', views.ActiveView.as_view(), name='active'),
    re_path(r'^send-active-email', views.SendActiveEmailView.as_view(), name='send-active-email'),
    re_path(r'^login/', views.LoginView.as_view(), name='login'),
    re_path(r'^logout/', views.LogoutView.as_view(), name='logout'),
    re_path(r'^$', views.UserInfoView.as_view(), name='user'),
    re_path(r'^order/(?P<page>\d+)$', views.UserOrderView.as_view(), name='order'),
    re_path(r'^address/$', views.AddressView.as_view(), name='address'),
]