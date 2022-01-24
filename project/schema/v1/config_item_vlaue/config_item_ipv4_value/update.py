#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel
from ipaddress import IPv4Address


class UpdateConfigItemIPV4ValueParams(BaseModel):
    """ 更新配置项IPV4值请求参数 """
    value: t.Optional[IPv4Address] = Field(alias='value', description='配置项IPV4值')
