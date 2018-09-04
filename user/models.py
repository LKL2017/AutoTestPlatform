from django.db import models


# Create your models here.


class Users(models.Model):
    """
    设置数据库
    name:用户名
    password:用户密码
    last_login_time:上一次登录时间
    create_time:首次登录时间
    privilege:权限
    id:自增主键
    """
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    last_login_time = models.DateTimeField()
    create_time = models.DateTimeField()
    privilege = models.IntegerField()
    id = models.AutoField(primary_key=True)


class Privileges(models.Model):
    """
    设置数据库
    """
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
