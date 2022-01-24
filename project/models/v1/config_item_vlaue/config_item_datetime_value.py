#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy_utils as su

from sqlalchemy.orm import relationship
from project.models.base import BaseModel


class ConfigItemDatetimeValueModel(BaseModel, su.Timestamp):
    """ 配置项日期时间值模型 """
    __tablename__ = 'ci_datetime_value'
    __table_args__ = (
        # 字典配置必须放最底部
        {'comment': '配置项日期时间值'},
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, comment='配置项日期值ID')
    value = sa.Column(sa.DateTime, nullable=False, comment='配置项日期时间值')

    ci_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci.id'), nullable=False, comment='配置项ID')
    ci_type_attribute_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci_type_attribute.id'), comment='配置项类型属性id')

    ci = relationship('ConfigItemModel', foreign_keys=[ci_id], backref='ci_ci_datetime_values')
    ci_type_attribute = relationship('ConfigItemTypeAttributeModel', foreign_keys=[ci_type_attribute_id], backref='ci_type_attribute_ci_datetime_values')
