#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotFoundConfigItemTimezoneValueError(RemoteError):
    """ 未找到配置项时区值错误 """
    pass
