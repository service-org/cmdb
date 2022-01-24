#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class ConfigItemFloatValueSchema(BaseModel):
    """ 单个配置项浮点值模式 """
    id: int = Field(alias='id', description='配置项浮点值ID')
    value: float = Field(alias='value', description='配置项浮点值')
    ci_id: int = Field(alias='ci_id', description='配置项ID')
    ci_type_attribute_id: int = Field(alias='ci_type_attribute_id', description='配置项类型属性id')

    class Config:
        orm_mode = True


class ListConfigItemFloatValueSchema(BaseModel):
    """ 列表配置项浮点值模式 """
    __root__: t.List[ConfigItemFloatValueSchema]
