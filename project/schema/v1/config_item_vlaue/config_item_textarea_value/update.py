#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemTextareaValueParams(BaseModel):
    """ 更新配置项文本域值请求参数 """
    value: t.Optional[t.Text] = Field(alias='value', description='配置项文本域值')
