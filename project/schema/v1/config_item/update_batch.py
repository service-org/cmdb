#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class ConfigItemSchema(BaseModel):
    """ 配置项模式 """
    ci_type_attribute_id: int = Field(alias='ci_type_attribute_id', description='配置项类型属性ID')
    value: t.Any = Field(alias='value', description='配置项值数据')


class UpdateBatchConfigItemParams(BaseModel):
    """ 批量更新配置项请求参数 """
    ci_id_list: t.List[int] = Field(alias='ci_id_list', description='配置项ID列表')
    ci_values: t.List[ConfigItemSchema] = Field(alias='ci_values', description='配置项值列表')
