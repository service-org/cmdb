#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.exception import RemoteError


class DuplicatedRelationError(RemoteError):
    """ 重复的关联关系错误 """
    pass
