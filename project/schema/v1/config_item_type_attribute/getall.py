#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from pydantic import Field
from pydantic import BaseModel
from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeValueType


class GetallConfigItemTypeAttributeParams(BaseModel):
    """ 获取所有配置项类型属性请求参数 """
    ci_type_attribute_group_id: int = Field(alias='ci_type_attribute_group_id', description='配置项类型属性分组id')


class ConfigItemTypeAttributeSchema(BaseModel):
    """ 配置项类型属性模式 """
    id: int = Field(alias='id', description='配置项类型属性ID')
    code: t.Text = Field(alias='code', description='配置项类型属性编码')
    name: t.Text = Field(alias='name', description='配置项类型属性名称')
    order: int = Field(alias='order', description='配置项类型属性排序')
    value_type: ConfigItemTypeAttributeValueType = Field(alias='value_type', description='配置项类型属性值类型')
    value_is_editable: bool = Field(alias='value_is_editable', description='配置项类型属性值是否可编辑?')
    value_is_required: bool = Field(alias='value_is_required', description='配置项类型属性值是否必填?')
    value_is_password: bool = Field(alias='value_is_password', description='配置项类型属性值是否密码?')
    value_is_url_link: bool = Field(alias='value_is_url_link', description='配置项类型属性值是否链接?')
    value_re_patterns: t.Union[bool, None] = Field(alias='value_re_patterns', description='配置项类型属性值正则校验表达式?')
    value_ge_limit_nu: t.Union[bool, None] = Field(alias='value_ge_limit_nu', description='配置项类型属性值最小值?')
    value_le_limit_nu: t.Union[bool, None] = Field(alias='value_le_limit_nu', description='配置项类型属性值最大值?')
    tips: t.Text = Field(alias='tips', description='配置项类型属性提示')
    ci_type_attribute_group_id: int = Field(alias='ci_type_attribute_group_id', description='配置项类型属性分组id')

    class Config:
        orm_mode = True


class ListConfigItemTypeAttributeSchema(BaseModel):
    """ 配置项类型属性列表模式 """
    __root__: t.List[ConfigItemTypeAttributeSchema]
