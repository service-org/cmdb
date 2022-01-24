#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from datetime import time
from pydantic import Field
from pydantic import BaseModel


class CreateConfigItemTimeValueParams(BaseModel):
    """ 创建配置项时间值请求参数 """
    value: time = Field(alias='value', description='配置项时间值')
    ci_id: int = Field(alias='ci_id', description='配置项ID')
    ci_type_attribute_id: int = Field(alias='ci_type_attribute_id', description='配置项类型属性id')
