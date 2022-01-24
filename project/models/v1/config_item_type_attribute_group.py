#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy_utils as su

from sqlalchemy.orm import relationship
from project.models.base import BaseModel


class ConfigItemTypeAttributeGroupModel(BaseModel, su.Timestamp):
    """ 配置项类型属性分组模型 """
    __tablename__ = 'ci_type_attribute_group'
    __table_args__ = (
        sa.UniqueConstraint('ci_type_id', 'code'),
        # 字典配置必须放最底部
        {'comment': '配置项类型属性分组'},
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, comment='配置项类型属性分组ID')
    code = sa.Column(sa.String(32), index=True, nullable=False, comment='配置项类型属性分组编码')
    name = sa.Column(sa.String(64), nullable=False, comment='配置项类型属性分组名称')
    order = sa.Column(sa.BigInteger, nullable=False, default=0, comment='配置项类型属性分组排序')
    is_collapse = sa.Column(sa.Boolean, nullable=False, default=False, comment='配置项类型属性分组是否折叠')

    ci_type_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci_type.id'), nullable=False, comment='配置项类型ID')

    ci_type = relationship('ConfigItemTypeModel', foreign_keys=[ci_type_id], backref='ci_type_ci_type_attribute_groups')
