#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 该方法用于提供User表的一些可能需要的查询操作

from user.models import User, Privilege


def user_dict() -> dict:
    """
    该表用于查询并且返回当前所有用户的id:name对应DICT

    """
    user_queryset = User.objects.all()
    return dict(
        [(user.id, user) for user in user_queryset]
    )


def privileges_id_name_dict() -> dict:
    """该方法用于返回当前所有权限的ID:NAME对应关系DICT"""
    p_queryset = Privilege.objects.all()
    return dict(
        [(p.id, p) for p in p_queryset]
    )
