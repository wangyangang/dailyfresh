# Generated by Django 2.2.3 on 2019-09-04 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20190904_0649'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '商品种类', 'verbose_name_plural': '商品种类'},
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=None, upload_to='type', verbose_name='商品类型图片'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='logo',
            field=models.CharField(default=None, max_length=20, verbose_name='标识'),
            preserve_default=False,
        ),
    ]
