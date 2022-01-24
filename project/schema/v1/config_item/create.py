#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class CreateConfigItemParams(BaseModel):
    """ 创建配置项请求参数 """
    ci_type_id: int = Field(alias='ci_type_id', description='配置项类型ID')
    ci: t.Dict[t.Text, t.Any] = Field(alias='ci', description='配置项数据')


class ConfigItemSchema(BaseModel):
    """ 配置项模式 """
    id: int = Field(alias='id', description='配置项ID')
    ci_type_id: int = Field(alias='ci_type_id', description='配置项类型ID')

    class Config:
        orm_mode = True
