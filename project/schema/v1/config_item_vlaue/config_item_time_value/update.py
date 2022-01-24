#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from datetime import time
from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemTimeValueParams(BaseModel):
    """ 更新配置项时间值请求参数 """
    value: t.Optional[time] = Field(alias='value', description='配置项时间值')
