#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotAllowedDeleteConfigItemTypeThatHasReferencedError(RemoteError):
    """ 不允许删除存在配置项类型引用错误 """
    pass


class NotAllowedDeleteConfigItemTypeThatHasInstantiatedError(RemoteError):
    """ 不允许删除实例化的配置项类型错误 """
    pass
