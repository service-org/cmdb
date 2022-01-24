#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotFoundConfigItemTypeConfigItemTypesError(RemoteError):
    """ 未找到配置项类型与配置项类型关联关系错误 """
    pass
