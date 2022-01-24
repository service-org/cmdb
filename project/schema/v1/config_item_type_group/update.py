#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemTypeGroupParams(BaseModel):
    """ 更新配置项类型分组请求参数 """
    name: t.Optional[t.Text] = Field(alias='name', description='配置项类型分组名称')
