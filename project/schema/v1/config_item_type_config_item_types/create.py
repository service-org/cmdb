#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel
from project.models.v1.config_item_type_config_item_types import ConfigItemTypeConfigItemTypesConstraint


class CreateConfigItemTypeConfigItemTypesParams(BaseModel):
    """ 创建配置项类型与配置项类型关联关系请求参数 """
    desc: t.Text = Field(alias='desc', description='配置项类型与配置项类型关联关联描述')
    constraint: ConfigItemTypeConfigItemTypesConstraint = Field(alias='constraint', description='来源到目标的约束')
    ci_type_source_id: int = Field(alias='ci_type_source_id', description='来源配置项类型ID')
    ci_type_relation_id: int = Field(alias='ci_type_relation_id', description='配置项类型与配置项类型关联关系ID')
    ci_type_target_id: int = Field(alias='ci_type_target_id', description='目标配置项类型ID')


class ConfigItemTypeConfigItemTypesSchema(BaseModel):
    """ 配置项类型与配置项类型关联关系模式 """
    id: int = Field(alias='id', description='配置项类型属性ID')
    desc: t.Text = Field(alias='desc', description='配置项类型与配置项类型关联关系描述')
    constraint: ConfigItemTypeConfigItemTypesConstraint = Field(alias='constraint', description='来源到目标的约束')
    ci_type_source_id: int = Field(alias='ci_type_source_id', description='来源配置项类型ID')
    ci_type_relation_id: int = Field(alias='ci_type_relation_id', description='配置项类型与配置项类型关联关系ID')
    ci_type_target_id: int = Field(alias='ci_type_target_id', description='目标配置项类型ID')

    class Config:
        orm_mode = True
