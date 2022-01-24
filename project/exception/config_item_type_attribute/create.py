#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class DuplicatedConfigItemTypeAttributeError(RemoteError):
    """ 重复的配置项类型属性错误 """
    pass


class RequiredConfigItemTypeAttributeError(RemoteError):
    """ 必须存在的配置项类型属性错误 """
    pass
