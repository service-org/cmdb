#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotAllowedDeleteGroupThatHasConfigItemTypeError(RemoteError):
    """ 不允许删除存在配置项类型的分组错误 """
    pass
