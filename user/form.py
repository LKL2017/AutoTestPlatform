#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 表单验证类

from django.forms import *
from user.models import User


class LoginForm(Form):
    username = CharField(max_length=50, min_length=1, required=True, error_messages={"required": "用户名不能为空!"})
    userpass = CharField(max_length=50, min_length=4, required=True, error_messages={"required": "密码不能为空!"})
    stay_login = BooleanField(required=False)

    def clean(self):
        username = self.cleaned_data["username"]
        exist = User.objects.filter("username").count()
        if not exist:
            raise forms.ValidationError("用户名不存在!")
        else:
            self.cleaned_data["username"] = username
