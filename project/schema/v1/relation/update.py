#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel
from project.models.v1.relation import RelationDirection


class UpdateRelationParams(BaseModel):
    """ 更新配置项类型分组请求参数 """
    name: t.Optional[t.Text] = Field(alias='name', description='配置项类型分组名称')
    source_to_target_desc: t.Optional[t.Text] = Field(alias='source_to_target_desc', description='源头到目标关系类型描述')
    target_to_source_desc: t.Optional[t.Text] = Field(alias='target_to_source_desc', description='目标到源头关系类型描述')
    direction: t.Optional[RelationDirection] = Field(alias='direction', description='关系方向')
