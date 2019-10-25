from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


class User(BaseModel, AbstractUser):
    class Meta:
        db_table = 'user'


class AddressManager(models.Manager):
    '''地址模型管理器类'''
    # 1.改变原有查询的结果集:all()
    # 2.封装方法:用户操作模型类对应的数据表(增删改查)
    def get_default_address(self, user):
        '''获取用户默认收货地址'''
        # self.model:获取self对象所在的模型类
        try:
            address = self.get(user=user, is_default=True)  # models.Manager
        except self.model.DoesNotExist:
            # 不存在默认收货地址
            address = None

        return address


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField('收件人', max_length=20)
    receiver_address = models.CharField('收件地址', max_length=50)
    post_code = models.CharField('邮编', max_length=10)
    phone_number = models.CharField('联系方式', max_length=11)
    is_default = models.NullBooleanField('是否默认')

    class Meta:
        db_table = 'address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name

    # 自定义一个模型管理器对象
    objects = AddressManager()

    def __str__(self):
        return self.receiver
