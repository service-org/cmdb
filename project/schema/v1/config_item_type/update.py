#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemTypeParams(BaseModel):
    """ 更新配置项类型请求参数 """
    name: t.Optional[t.Text] = Field(alias='name', description='配置项类型名称')
    icon: t.Optional[t.Text] = Field(alias='icon', description='是否是停用的配置项类型?')
    desc: t.Optional[t.Text] = Field(alias='desc', description='配置项类型描述')
    is_disabled: t.Optional[bool] = Field(alias='is_disabled', description='是否是停用的配置项类型?')
