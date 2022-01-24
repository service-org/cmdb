#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from datetime import time
from pydantic import Field
from pydantic import BaseModel


class ConfigItemTimeValueSchema(BaseModel):
    """ 单个配置项时间值模式 """
    id: int = Field(alias='id', description='配置项时间值ID')
    value: time = Field(alias='value', description='配置项时间值')
    ci_id: int = Field(alias='ci_id', description='配置项ID')
    ci_type_attribute_id: int = Field(alias='ci_type_attribute_id', description='配置项类型属性id')

    class Config:
        orm_mode = True
        json_encoders = {
            time: lambda v: v.strftime('%H:%M:%S')
        }


class ListConfigItemTimeValueSchema(BaseModel):
    """ 列表配置项时间值模式 """
    __root__: t.List[ConfigItemTimeValueSchema]
