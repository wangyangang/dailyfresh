"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf import settings
from django.contrib.staticfiles.views import serve


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', include('haystack.urls')),
    path('', include(('goods.urls', 'goods'), namespace='goods')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),

    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
]
