#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 该模块用户定义在传输过程的数据模型，应该不是Django所推荐使用的方法，不过可以一试


class ProductData:
    """
    字段说明：
    name:产品名
    create_user:产品创建者的名字
    incharge_user:负责人的名字
    create_time:创建时间
    status:产品状态
    """

    def __init__(self, name, create_user, incharge_user, create_time, status):
        self.name = name
        self.create_user = create_user
        self.incharge_user = incharge_user
        self.create_time = create_time
        self.status = status

    def __str__(self):
        return str("产品的名字为:" + self.name + " at :" + id(self))
