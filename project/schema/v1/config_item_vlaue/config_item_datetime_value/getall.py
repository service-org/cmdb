#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from datetime import datetime
from pydantic import BaseModel


class ConfigItemDatetimeValueSchema(BaseModel):
    """ 单个配置项日期时间值模式 """
    id: int = Field(alias='id', description='配置项日期时间值ID')
    value: datetime = Field(alias='value', description='配置项日期时间值')
    ci_id: int = Field(alias='ci_id', description='配置项ID')
    ci_type_attribute_id: int = Field(alias='ci_type_attribute_id', description='配置项类型属性id')

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }


class ListConfigItemDatetimeValueSchema(BaseModel):
    """ 列表配置项日期时间值模式 """
    __root__: t.List[ConfigItemDatetimeValueSchema]
