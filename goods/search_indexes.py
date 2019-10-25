from haystack import indexes
from .models import Goods_SKU


# 指定对于某个类的某些数据建立索引
class Good_SKUIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Goods_SKU

    def index_queryset(self, using=None):
        return self.get_model().objects.all()