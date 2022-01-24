#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import BaseModel


class DeleteBatchConfigItemParams(BaseModel):
    """ 批量删除配置项请求参数 """
    __root__: t.List[int]
