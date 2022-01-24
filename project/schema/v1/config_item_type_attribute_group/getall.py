#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class GetallConfigItemTypeAttributeGroupParams(BaseModel):
    """ 获取所有配置项类型属性分组请求参数 """
    ci_type_id: int = Field(alias='ci_type_id', description='配置项类型ID')
