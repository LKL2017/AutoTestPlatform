from django.db import models


# Create your models here.


class TestCase(models.Model):
    """
    测试用例的数据模型
    字段说明：
    title:测试用例标题  text
    precondition: 前置条件 text
    steps:步骤
    expect:期望
    create_user:创建者 integer
    create_time:创建时间 dateTime
    last_edit_user:最后编辑者 integer
    last_edit_time:最后编辑时间 dateTime
    editable:可编辑状态 boolean
    case_module:所属模块 Integer
    """
    title = models.TextField(null=False, unique=True)
    precondition = models.TextField(default="")
    steps = models.TextField(null=False)
    expect = models.TextField(null=False)
    create_user = models.IntegerField(null=False)
    create_time = models.DateTimeField(auto_now=True)
    last_edit_user = models.IntegerField()
    last_edit_time = models.DateTimeField()
    case_module = models.IntegerField()
    editable = models.BooleanField(default=True)

    def __init__(self):
        super(TestCase, self).__init__()
        if self.last_edit_time is None:
            self.last_edit_time = self.create_time
        if self.last_edit_user is None:
            self.last_edit_user = self.create_user


class CaseModule(models.Model):
    """
    模块的数据模型
    字段说明：
    name:模块名称
    create_time: 创建时间
    create_user: 创建者
    desc: 描述
    """
    name = models.CharField(max_length=255, unique=True)
    create_time = models.DateTimeField(auto_now=True)
    create_user = models.IntegerField()
    desc = models.TextField()
