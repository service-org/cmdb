#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemUserValueParams(BaseModel):
    """ 更新配置项用户值请求参数 """
    value: t.Optional[int] = Field(alias='value', description='配置项用户值')
