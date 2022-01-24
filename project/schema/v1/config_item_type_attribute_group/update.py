#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemTypeAttributeGroupParams(BaseModel):
    """ 更新配置项类型属性分组请求参数 """
    name: t.Optional[t.Text] = Field(alias='name', description='配置项类型属性分组名称')
    order: t.Optional[int] = Field(alias='order', description='配置项类型属性分组排序')
    is_collapse: t.Optional[bool] = Field(alias='is_collapse', description='配置项类型属性分组是否折叠')
