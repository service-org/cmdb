#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy_utils as su

from enum import Enum
from sqlalchemy.orm import relationship
from project.models.base import BaseModel


class ConfigItemTypeAttributeValueType(Enum):
    """ 配置项类型属性值类型 """
    FLOAT = 'float'
    INT = 'int'
    IPV4 = 'ipv4'
    DATE = 'date'
    TIME = 'time'
    TEXT = 'text'
    BOOL = 'bool'
    USER = 'user'
    JSON = 'json'
    TEXTAREA = 'textarea'
    TIMEZONE = 'timezone'
    DATETIME = 'datetime'


class ConfigItemTypeAttributeModel(BaseModel, su.Timestamp):
    """ 配置项类型属性模型 """
    __tablename__ = 'ci_type_attribute'
    __table_args__ = (
        sa.UniqueConstraint('ci_type_attribute_group_id', 'code'),
        sa.UniqueConstraint('ci_type_attribute_group_id', 'name'),
        # 字典配置必须放最底部
        {'comment': '配置项类型属性'},
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, comment='配置项类型属性ID')
    code = sa.Column(sa.String(32), index=True, nullable=False, comment='配置项类型属性编码')
    name = sa.Column(sa.String(64), nullable=False, comment='配置项类型属性名称')
    order = sa.Column(sa.BigInteger, nullable=False, default=0, comment='配置项类型属性排序')
    value_type = sa.Column(sa.Enum(ConfigItemTypeAttributeValueType), nullable=False, default=ConfigItemTypeAttributeValueType.TEXT, comment='配置项类型属性值类型')
    value_is_editable = sa.Column(sa.Boolean, nullable=False, default=True, comment='配置项类型属性值是否可编辑?')
    value_is_required = sa.Column(sa.Boolean, nullable=False, default=False, comment='配置项类型属性值是否必填?')
    value_is_password = sa.Column(sa.Boolean, nullable=False, default=False, comment='配置项类型属性值是否密码?')
    value_is_url_link = sa.Column(sa.Boolean, nullable=False, default=False, comment='配置项类型属性值是否链接?')
    value_re_patterns = sa.Column(sa.Text, nullable=True, default=None, comment='配置项类型属性值正则校验表达式')
    value_ge_limit_nu = sa.Column(sa.BigInteger, nullable=True, default=None, comment='配置项类型属性值最小值')
    value_le_limit_nu = sa.Column(sa.BigInteger, nullable=True, default=None, comment='配置项类型属性值最大值')
    tips = sa.Column(sa.Text, nullable=False, default='', comment='配置项类型属性提示')

    ci_type_attribute_group_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci_type_attribute_group.id'), nullable=False, comment='配置项类型属性分组ID')

    ci_type_attribute_group = relationship('ConfigItemTypeAttributeGroupModel', foreign_keys=[ci_type_attribute_group_id], backref='ci_type_attribute_group_ci_type_attributes')
