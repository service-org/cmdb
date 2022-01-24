#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotFoundConfigItemTypeAttributeError(RemoteError):
    """ 未找到配置项类型属性错误 """
    pass
