from django.db import models


# Create your models here.


class Product(models.Model):
    """
    各个字段的说明：
    name:产品名
    user_in_charge:产品的负责人
    create_user:产品的创建者
    create_time:产品的创建时间
    description:产品的描述
    """
    name = models.CharField(max_length=255, unique=True, null=False)
    inChargeUser = models.IntegerField(max_length=4, null=False)
    createUser = models.IntegerField(max_length=4, null=False)
    createTime = models.DateField(auto_now=True)
    description = models.TextField()
