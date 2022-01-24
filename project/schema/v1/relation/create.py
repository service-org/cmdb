#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel
from project.models.v1.relation import RelationDirection


class CreateRelationParams(BaseModel):
    """ 创建关联关系请求参数 """
    code: t.Text = Field(alias='code', description='关联类型编码')
    name: t.Text = Field(alias='name', description='关联类型名称')
    is_built_in: t.Optional[bool] = Field(alias='is_built_in', description='是否是内置的关系类型?')
    source_to_target_desc: t.Text = Field(alias='source_to_target_desc', description='源头到目标关系类型描述')
    target_to_source_desc: t.Text = Field(alias='target_to_source_desc', description='目标到源头关系类型描述')
    direction: t.Optional[RelationDirection] = Field(alias='direction', description='关系方向')


class RelationSchema(BaseModel):
    """ 关联关系模式 """
    id: int = Field(alias='id', description='配置项类型分组ID')
    code: t.Text = Field(alias='code', description='关联类型编码')
    name: t.Text = Field(alias='name', description='关联类型名称')
    is_built_in: bool = Field(alias='is_built_in', description='是否是内置的关系类型?')
    source_to_target_desc: t.Text = Field(alias='source_to_target_desc', description='源头到目标关系类型描述')
    target_to_source_desc: t.Text = Field(alias='target_to_source_desc', description='目标到源头关系类型描述')
    direction: t.Optional[RelationDirection] = Field(alias='direction', description='关系方向')

    class Config:
        orm_mode = True
