#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class DuplicatedConfigItemTypeGroupError(RemoteError):
    """ 重复的配置项类型分组错误 """
    pass
