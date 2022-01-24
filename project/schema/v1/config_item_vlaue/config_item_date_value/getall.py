#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from datetime import date
from pydantic import Field
from pydantic import BaseModel


class ConfigItemDateValueSchema(BaseModel):
    """ 单个配置项日期值模式 """
    id: int = Field(alias='id', description='配置项日期值ID')
    value: date = Field(alias='value', description='配置项日期值')
    ci_id: int = Field(alias='ci_id', description='配置项ID')
    ci_type_attribute_id: int = Field(alias='ci_type_attribute_id', description='配置项类型属性id')

    class Config:
        orm_mode = True
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d')
        }


class ListConfigItemDateValueSchema(BaseModel):
    """ 列表配置项日期值模式 """
    __root__: t.List[ConfigItemDateValueSchema]
