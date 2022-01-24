#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from pydantic import Field
from datetime import datetime
from pydantic import BaseModel


class CreateConfigItemDatetimeValueParams(BaseModel):
    """ 创建配置项日期时间值请求参数 """
    value: datetime = Field(alias='value', description='配置项日期时间值')
    ci_id: int = Field(alias='ci_id', description='配置项ID')
    ci_type_attribute_id: int = Field(alias='ci_type_attribute_id', description='配置项类型属性id')
