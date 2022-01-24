#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class CreateConfigItemTypeGroupParams(BaseModel):
    """ 创建配置项类型分组请求参数 """
    code: t.Text = Field(alias='code', description='配置项类型分组编码')
    name: t.Text = Field(alias='name', description='配置项类型分组名称')


class ConfigItemTypeGroupSchema(BaseModel):
    """ 配置项类型分组模式 """
    id: int = Field(alias='id', description='配置项类型分组ID')
    code: t.Text = Field(alias='code', description='配置项类型分组编码')
    name: t.Text = Field(alias='name', description='配置项类型分组名称')
    is_built_in: bool = Field(alias='is_built_in', description='是否是内置的配置项类型分组?')
    order: int = Field(alias='order', description='配置项类型分组排序')

    class Config:
        orm_mode = True
