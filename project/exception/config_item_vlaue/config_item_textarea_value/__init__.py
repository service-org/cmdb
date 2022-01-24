#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotFoundConfigItemTextareaValueError(RemoteError):
    """ 未找到配置项文本域值错误 """
    pass
