#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class CreateConfigItemTypeAttributeGroupParams(BaseModel):
    """ 创建配置项类型属性分组请求参数 """
    code: t.Text = Field(alias='code', description='配置项类型分组编码')
    name: t.Text = Field(alias='name', description='配置项类型分组名称')
    ci_type_id: int = Field(alias='ci_type_id', description='配置项类型ID')


class ConfigItemTypeAttributeGroupSchema(BaseModel):
    """ 配置项类型分组模式 """
    id: int = Field(alias='id', description='配置项类型分组ID')
    code: t.Text = Field(alias='code', description='配置项类型分组编码')
    name: t.Text = Field(alias='name', description='配置项类型分组名称')
    order: int = Field(alias='order', description='配置项类型分组排序')
    is_collapse: bool = Field(alias='is_collapse', description='是否折叠显示配置项类型分组?')
    ci_type_id: int = Field(alias='ci_type_id', description='配置项类型ID')

    class Config:
        orm_mode = True
