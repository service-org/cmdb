#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class GetallConfigItemParams(BaseModel):
    """ 获取所有配置项请求参数 """
    page: t.Optional[int] = Field(alias='page', ge=1, description='当前页码')
    page_size: t.Optional[int] = Field(alias='page_size', ge=1, le=200, description='分页大小')
    ci_type_id: int = Field(alias='ci_type_id', description='配置项类型ID')
