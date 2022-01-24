#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Json
from pydantic import Field
from pydantic import BaseModel


class ConfigItemJsonValueSchema(BaseModel):
    """ 单个配置项JSON值模式 """
    id: int = Field(alias='id', description='配置项JSON值ID')
    value: Json = Field(alias='value', description='配置项JSON值')
    ci_id: int = Field(alias='ci_id', description='配置项ID')
    ci_type_attribute_id: int = Field(alias='ci_type_attribute_id', description='配置项类型属性id')

    class Config:
        orm_mode = True


class ListConfigItemJsonValueSchema(BaseModel):
    """ 列表配置项JSON值模式 """
    __root__: t.List[ConfigItemJsonValueSchema]
