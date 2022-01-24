#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class NotAllowedDeleteRelationThatHasReferencedError(RemoteError):
    """ 不允许删除存在被引用错误 """
    pass
