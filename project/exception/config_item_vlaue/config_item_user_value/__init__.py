#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotFoundConfigItemUserValueError(RemoteError):
    """ 未找到配置项用户值错误 """
    pass
