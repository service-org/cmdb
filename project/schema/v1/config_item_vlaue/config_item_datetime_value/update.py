#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from datetime import datetime
from pydantic import BaseModel


class UpdateConfigItemDatetimeValueParams(BaseModel):
    """ 更新配置项日期时间值请求参数 """
    value: t.Optional[datetime] = Field(alias='value', description='配置项日期时间值')
