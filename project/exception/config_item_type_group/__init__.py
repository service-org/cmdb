#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotFoundConfigItemTypeGroupError(RemoteError):
    """ 未找到配置项类型分组错误 """
    pass
