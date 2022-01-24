#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel


class UpdateConfigItemTypeAttributeParams(BaseModel):
    """ 更新配置项类型属性请求参数 """
    name: t.Optional[t.Text] = Field(alias='name', description='配置项类型属性名称')
    order: t.Optional[int] = Field(alias='order', description='配置项类型属性排序')
    value_is_editable: t.Optional[bool] = Field(alias='value_is_editable', description='配置项类型属性值是否可编辑?')
    value_is_required: t.Optional[bool] = Field(alias='value_is_required', description='配置项类型属性值是否必填?')
    value_is_password: t.Optional[bool] = Field(alias='value_is_password', description='配置项类型属性值是否密码?')
    value_is_url_link: t.Optional[bool] = Field(alias='value_is_url_link', description='配置项类型属性值是否链接?')
    value_re_patterns: t.Optional[t.Union[bool, None]] = Field(alias='value_re_patterns', description='配置项类型属性值正则校验表达式?')
    value_ge_limit_nu: t.Optional[t.Union[bool, None]] = Field(alias='value_ge_limit_nu', description='配置项类型属性值最小值?')
    value_le_limit_nu: t.Optional[t.Union[bool, None]] = Field(alias='value_le_limit_nu', description='配置项类型属性值最大值?')
    tips: t.Optional[t.Text] = Field(alias='tips', description='配置项类型属性提示')
