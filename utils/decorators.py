#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 部分用于使用的工具装饰器
from django.shortcuts import render


def dec_is_login(func):
    print(func.__name__)

    def wrapped(request, *args, **kwargs):
        try:
            user = request.sesson.get("user", None)
            print(user)
        except AttributeError:
            return render(request, "login.html", {"error_not_login": "请重新登录!"})
        else:
            if user:
                print(user)
                return func(request, *args, **kwargs)

    return wrapped
