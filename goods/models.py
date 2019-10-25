from django.db import models
from db.base_model import BaseModel


class Category(BaseModel):
    name = models.CharField('名称', max_length=20)
    logo = models.CharField(max_length=20, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='商品类型图片')

    class Meta:
        db_table = 'category'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods_SPU(BaseModel):
    name = models.CharField('名称', max_length=20)
    detail = models.CharField('详情', max_length=100)

    class Meta:
        db_table = 'goods_spu'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods_SKU(BaseModel):
    name = models.CharField('名称', max_length=50)
    summary = models.TextField('简介', max_length=200)
    price = models.DecimalField('价格', max_digits=8, decimal_places=2)
    unit = models.CharField('单位', max_length=20)
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    stock = models.PositiveIntegerField('库存')
    sales = models.PositiveIntegerField('销量')
    category = models.ForeignKey(Category, on_delete=None)
    spu = models.ForeignKey(Goods_SPU, on_delete=None)

    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexGoodsBanner(BaseModel):
    '''首页轮播商品展示模型类'''
    sku = models.ForeignKey(Goods_SKU, verbose_name='商品', on_delete=None)
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序') # 0 1 2 3

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name


class IndexPromotionBanner(BaseModel):
    '''首页促销活动模型类'''
    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.CharField(max_length=256, verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = "主页促销活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexTypeGoodsBanner(BaseModel):
    '''首页分类商品展示模型类'''
    DISPLAY_TYPE_CHOICES = (
        (0, "标题"),
        (1, "图片")
    )

    type = models.ForeignKey(Category, verbose_name='商品类型', on_delete=None)
    sku = models.ForeignKey(Goods_SKU, verbose_name='商品SKU', on_delete=None)
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = "主页分类展示商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name