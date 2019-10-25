from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from goods.models import Goods_SKU
from django_redis import get_redis_connection

from goods.models import Goods_SKU
from utils.mixin import LoginrequiredMixin


class CartInfoView(LoginrequiredMixin, View):
    def get(self, request):
        '''显示'''
        # 获取登录的用户
        user = request.user
        # 获取用户购物车中商品的信息
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        # {'商品id':商品数量, ...}
        cart_dict = conn.hgetall(cart_key)

        skus = []
        # 保存用户购物车中商品的总数目和总价格
        total_count = 0
        total_price = 0
        # 遍历获取商品的信息
        for sku_id, count in cart_dict.items():
            # 根据商品的id获取商品的信息
            sku = Goods_SKU.objects.get(id=sku_id)
            # 计算商品的小计
            amount = sku.price*int(count)
            # 动态给sku对象增加一个属性amount, 保存商品的小计
            sku.amount = amount
            # 动态给sku对象增加一个属性count, 保存购物车中对应商品的数量
            sku.count = int(count)
            # 添加
            skus.append(sku)

            # 累加计算商品的总数目和总价格
            total_count += int(count)
            total_price += amount

        # 组织上下文
        context = {'total_count':total_count,
                   'total_price':total_price,
                   'skus':skus}

        # 使用模板
        return render(request, 'cart.html', context)


class CartAddView(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 接受数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        if not all([sku_id, count]):
            return JsonResponse({'errno': 1, 'errmsg': '数据不完整'})

        # 校验商品的数量
        try:
            count = int(count)
        except Exception:
            return JsonResponse({'errno': 2, 'errmsg': '商品数量出错'})

        # 校验商品是否存在
        try:
            sku = Goods_SKU.objects.get(id=sku_id)
        except Goods_SKU.DoesNotExist:
            return JsonResponse({'errno': 3, 'errmsg': '商品不存在'})

        # 业务处理：添加购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        # 先尝试获取数据库里的sku_id的值 => hget(cart_key, sku_id),
        # 返回None表示商品在购物车不存在
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            count += int(cart_count)

        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'errno': 4, 'errmsg': '库存不足'})

        # 设置redis库里cart_key 对应的值，如果sku_id存在，更新数据，如果不存在，添加数据。
        conn.hset(cart_key, sku_id, count)
        # 计算用户购物车商品的条目数
        total_count = conn.hlen(cart_key)

        return JsonResponse({'errno': 5, 'errmsg': '添加成功', 'total_count': total_count})


class CartUpdateView(View):
    def post(self, request):
        # sku_id, count
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        if not all([sku_id, count]):
            return JsonResponse({'errno': 0, 'errmsg': '数据不完整'})
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'errno': 1, 'errmsg': '未登录'})

        try:
            count = int(count)
        except Exception:
            return JsonResponse({'errno': 2, 'errmsg': '商品数目出错'})

        try:
            sku = Goods_SKU.objects.get(id=sku_id)
        except Goods_SKU.DoesNotExist:
            return JsonResponse({'errno': 3, 'errmsg': '商品不存在'})

        if count > sku.stock:
            return JsonResponse({'errno': 4, 'errmsg': '库存不足'})

        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        conn.hset(cart_key, sku_id, count)

        # 计算购物车商品总件数
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        return JsonResponse({"errno": 5, 'errmsg': '成功', 'total_count': total_count})