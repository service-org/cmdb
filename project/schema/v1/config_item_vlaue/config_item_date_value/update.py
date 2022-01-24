#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from datetime import date
from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemDateValueParams(BaseModel):
    """ 更新配置项日期值请求参数 """
    value: t.Optional[date] = Field(alias='value', description='配置项日期值')
