from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from utils.response_code import RET, error_map
from user.models import User
from .models import Address
from orders.models import OrderInfo, OrderGoods
from goods.models import Goods_SKU
from utils.mixin import LoginrequiredMixin
from django_redis import get_redis_connection
from django.http import Http404
from celery_tasks.tasks import send_active_email_async


def send_active_email(user):
    # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
    # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密

    # 加密用户的身份信息，生成激活token
    serializer = Serializer(settings.SECRET_KEY, 3600)
    info = {'confirm': user.id}
    token = serializer.dumps(info)
    token = token.decode()

    # 组织邮件信息
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [user.email]
    html_message = '<h1>%s,</h1>请点击下面链接激活您的账户<br/>' \
                   '<a href="http://127.0.0.1:8000/user/active/%s">' \
                   'http://127.0.0.1:8000/user/active/%s</a>' % (user.username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)


# /user/register
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        if not all([user_name, pwd, cpwd, email]):
            return JsonResponse({'errno': RET.PARAMERR, 'errmsg': error_map[RET.PARAMERR]})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return JsonResponse({'errno': RET.THIRDERR, 'errmsg': error_map[RET.THIRDERR]})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return JsonResponse({'errno': RET.DATAEXIST, 'errmsg': error_map[RET.DATAEXIST]})

        user = User.objects.create_user(user_name, email, pwd)
        user.is_active = 0
        user.save()

        # send_active_email(user)
        print(user.id, user.username, user.email)
        send_active_email_async.delay(user.id, user.username, user.email)

        response = JsonResponse({'errno': RET.OK, 'errmsg': error_map[RET.OK]})
        response.set_cookie('inactive_user_id', user.id, 1*24*3600)

        inactive_user_id = request.COOKIES.get('inactive_user_id')
        print('inactivate_user_id %s' % inactive_user_id)

        return response


class SendActiveEmailView(View):
    def get(self, request):
        user_id = request.COOKIES.get('inactive_user_id')
        inactive_user = User.objects.get(id=int(user_id))
        # send_active_email(inactive_user)

        send_active_email_async.delay(inactive_user.id, inactive_user.username, inactive_user.email)

        s1 = '''<div style="text-align:center;">
                邮件已发送<br>
                <a href="/user/send-active-email/">重新发送激活邮件</a><br>
                <a href="/user/login/">立即登录</a>
                </div>'''
        return HttpResponse(s1)


class ActiveView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            response = redirect(reverse('user:login'))

            # 去掉cookie保存的未激活的email
            unverified_email = request.COOKIES.get('unverified_email')
            if user.email == unverified_email:
                response.delete_cookie('unvefied_email')

            return response
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期')


# /user/unverified-email/
class UnverifiedEmail(View):
    def get(self, request):
        if not request.user.is_authenticated:
            # 从cookie里获取未激活的用户id
            inactive_user_id = request.COOKIES.get('inactive_user_id')
            if inactive_user_id is None:
                raise Http404()
            user = User.objects.get(id=int(inactive_user_id))
            return render(request, 'unverified_email.html', {'user': user})
        else:
            return HttpResponse('用户已登录！')


class LoginView(View):
    def get(self, request):
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        print(request)
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        if not all([username, pwd]):
            return JsonResponse({'errno': RET.PARAMERR, 'errmsg': error_map[RET.PARAMERR]})

        try:
            user = User.objects.get(username=username)
        except Exception:
            return JsonResponse({'errno': RET.PARAMERR, 'errmsg': '用户名不存在'})

        if not user.check_password(pwd):
            return JsonResponse({"errno": RET.PWDERR, 'errmsg': '密码错误'})

        if not user.is_active:
            response = JsonResponse({'errno': RET.USERERR, 'errmsg': '用户未激活'})
            response.set_cookie('inactive_user_id', user.id)
            return response
        # 用户名密码正确，已激活用户

        # 激活与否都让登录，可在个人中心激活账户
        login(request, user)
        next_url = request.GET.get('next', reverse('goods:index'))
        print('next_url: %s' % next_url)
        response = redirect(next_url)

        remember = request.POST.get('remember')
        if remember == 'on':
            response.set_cookie('username', username, 7*24*3600)
        else:
            response.delete_cookie('username')

        return JsonResponse({'errno': RET.OK, 'errmsg': error_map[RET.OK]})


# /user/logout
class LogoutView(LoginrequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse('goods:index'))


# /user
class UserInfoView(LoginrequiredMixin, View):
    def get(self, request):
        '''显示'''
        # Django会给request对象添加一个属性request.user
        # 如果用户未登录->user是AnonymousUser类的一个实例对象
        # 如果用户登录->user是User类的一个实例对象
        # request.user.is_authenticated()

        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取用户的历史浏览记录
        # from redis import StrictRedis
        # sr = StrictRedis(host='172.16.179.130', port='6379', db=9)
        con = get_redis_connection('default')

        history_key = 'history_%d'%user.id

        # 获取用户最新浏览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4) # [2,3,1]

        # 从数据库中查询用户浏览的商品的具体信息
        # goods_li = GoodsSKU.objects.filter(id__in=sku_ids)
        #
        # goods_res = []
        # for a_id in sku_ids:
        #     for goods in goods_li:
        #         if a_id == goods.id:
        #             goods_res.append(goods)

        # 遍历获取用户浏览的商品信息
        goods_li = []
        for id in sku_ids:
            goods = Goods_SKU.objects.get(id=id)
            goods_li.append(goods)

        # 组织上下文
        context = {'page':'user',
                   'address':address,
                   'goods_li':goods_li}

        # 除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件
        return render(request, 'user_center_info.html', context)


# /user/order
class UserOrderView(LoginrequiredMixin, View):
    '''用户中心-订单页'''
    def get(self, request, page):
        '''显示'''
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历获取订单商品的信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count*order_sku.price
                # 动态给order_sku增加属性amount,保存订单商品的小计
                order_sku.amount = amount

            # 动态给order增加属性，保存订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性，保存订单商品的信息
            order.order_skus = order_skus

        # 分页
        paginator = Paginator(orders, 1)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        order_page = paginator.page(page)

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 组织上下文
        context = {'order_page':order_page,
                   'pages':pages,
                   'page': 'order'}

        # 使用模板
        return render(request, 'user_center_order.html', context)


# /user/address
class AddressView(LoginrequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            addresses = Address.objects.filter(user=user)
        except Address.DoesNotExist:
            address = None
        return render(request, 'user_center_site.html', {'page': 'address', "addresses": addresses})

    def post(self, request):
        '''地址的添加'''
        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all([receiver, addr, phone, type]):
            return render(request, 'user_center_site.html', {'errmsg':'数据不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg':'手机格式不正确'})

        # 业务处理：地址添加
        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户对应User对象
        user = request.user
        print(user)

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None

        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               receiver_address=addr,
                               post_code=zip_code,
                               phone_number=phone,
                               is_default=is_default)

        # 返回应答,刷新地址页面
        return redirect(reverse('user:address'))  # get请求方式
