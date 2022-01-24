#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemTypeConfigItemTypesParams(BaseModel):
    """ 更新配置项类型与配置项类型关联关系请求参数 """
    desc: t.Text = Field(alias='desc', description='配置项类型与配置项类型关联关联描述')
