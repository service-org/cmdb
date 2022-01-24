#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class DuplicatedConfigItemTypeConfigItemTypesError(RemoteError):
    """ 重复的配置项类型与配置项类型关联关系错误 """
    pass
