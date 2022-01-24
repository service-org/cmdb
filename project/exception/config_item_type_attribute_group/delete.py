#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotAllowedDeleteGroupThatHasConfigItemTypeAttributeError(RemoteError):
    """ 不允许删除存在配置项类型属性的分组错误 """
    pass
