from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('修改时间',auto_now=True)
    is_delete = models.NullBooleanField('删除标记')

    class Meta:
        abstract = True

