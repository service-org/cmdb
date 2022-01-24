#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotFoundConfigItemTextValueError(RemoteError):
    """ 未找到配置项文本值错误 """
    pass
