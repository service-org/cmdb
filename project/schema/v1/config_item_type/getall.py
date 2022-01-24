#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class GetallConfigItemTypeParams(BaseModel):
    """ 获取所有配置项类型请求参数 """
    ci_type_group_id: int = Field(alias='ci_type_group_id', description='配置项类型分组id')


class ConfigItemTypeSchema(BaseModel):
    """ 配置项类型模式 """
    id: int = Field(alias='id', description='配置项类型ID')
    code: t.Text = Field(alias='code', description='配置项类型编码')
    name: t.Text = Field(alias='name', description='配置项类型名称')
    is_built_in: bool = Field(alias='is_built_in', description='是否是内置的配置项类型?')
    is_disabled: bool = Field(alias='is_disabled', description='是否是停用的配置项类型?')
    is_not_show: bool = Field(alias='is_not_show', description='是否要不显示配置项类型?')
    icon: t.Text = Field(alias='icon', description='配置项类型图标')
    desc: t.Text = Field(alias='desc', description='配置项类型描述')
    ci_type_group_id: int = Field(alias='ci_type_group_id', description='配置项类型分组id')

    class Config:
        orm_mode = True


class ListConfigItemTypeSchema(BaseModel):
    """ 配置项类型列表模式 """
    __root__: t.List[ConfigItemTypeSchema]
