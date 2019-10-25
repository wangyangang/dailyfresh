"""
Django settings for dailyfresh project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dd%=l$qf)1wi+_6%4%c($r=)09l17o%rk#i2jwmod$vrd+nn%o'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = []

SECRET_KEY = '27yjrm0sd1@ifpq%q4k376o4a)fd&$$v7ej(7)ag(#8tq%vr+-'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'haystack',
    'djcelery',
    'cart.apps.CartConfig',
    'goods.apps.GoodsConfig',
    'user.apps.UserConfig',
    'orders.apps.OrdersConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dailyfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dailyfresh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dailyfresh',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '456wyg31'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
AUTH_USER_MODEL = 'user.User'

# 全文检索框架的配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smpt服务地址
# EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST = 'smtpdm.aliyun.com'
# EMAIL_PORT = 25
EMAIL_PORT = 465
# 发送邮件的邮箱
# EMAIL_HOST_USER = 'cool3174@163.com'
EMAIL_HOST_USER = 'mail@wyg.wangyangang.com'
# 在邮箱中设置的客户端授权密码
# EMAIL_HOST_PASSWORD = '456wyg31'
EMAIL_HOST_PASSWORD = '456wygWYG31'
# 收件人看到的发件人
# EMAIL_FROM = '天天生鲜<cool3174@163.com>'
EMAIL_FROM = '天天生鲜<mail@wyg.wangyangang.com>'
EMAIL_USE_SSL = True   # 打开ssl协议

# Django的缓存配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://172.16.28.145:6379/9",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 设置Django的文件存储类
DEFAULT_FILE_STORAGE = 'utils.fdfs.storage.FDFSStorage'
# DEFAULT_FILE_STORAGE = 'utils.fdfs.storage1.FdfsStorage'

# 设置fdfs使用的client.conf文件路径
FDFS_CLIENT_CONF = './utils/fdfs/client.conf'

# 设置fdfs存储服务器上nginx的IP和端口号
#FDFS_URL = 'http://172.16.28.145:8888/'
FDFS_URL = 'https://172.16.28.145:443/'
LAST_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SERVER_IP = '120.25.224.111'
SERVER_IP = '172.16.28.145'

# CUSTOM_STORAGE_OPTIONS = {
#     'CLIENT_CONF': './utils/fdfs/client.conf',
#     'BASE_URL': SERVER_IP + ':8888/',
# }
CUSTOM_STORAGE_OPTIONS = {
    'CLIENT_CONF': './utils/fdfs/client.conf',
    'BASE_URL': SERVER_IP + ':443/',
}

# alipay设置
APP_ID = '2016092900626151'
APP_PRIVATE_KEY_PATH = 'orders/app_private_key.pem'
ALIPAY_PUBLIC_KEY_PATH = 'orders/alipay_public_key.pem'

# 配置登录url地址
LOGIN_URL = '/user/login' # /accounts/login?next=/user

# 商品列表页/list/type_id/page/页，每页展示的条数
GOODS_COUNT_PER_PAGE = 10

