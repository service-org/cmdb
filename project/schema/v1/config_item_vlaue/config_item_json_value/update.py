#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Json
from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemJsonValueParams(BaseModel):
    """ 更新配置项JSON值请求参数 """
    value: t.Optional[Json] = Field(alias='value', description='配置项JSON值')
