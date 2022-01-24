#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy_utils as su

from enum import Enum
from sqlalchemy.orm import relationship
from project.models.base import BaseModel

class ConfigItemTypeConfigItemTypesConstraint(Enum):
    """ 配置项类型与配置项类型关联关系约束 """
    # 多对多约束
    MTOM = 'm2m'
    # 一对多约束
    OTOM = 'o2m'
    # 一对一约束
    OTOO = 'o2o'

class ConfigItemTypeConfigItemTypesModel(BaseModel, su.Timestamp):
    """ 配置项类型与配置项类型关联关系模型 """
    __tablename__ = 'ci_type_ci_types'
    __table_args__ = (
        sa.UniqueConstraint('ci_type_source_id', 'ci_type_relation_id', 'ci_type_target_id'),
        # 字典配置必须放最底部
        {'comment': '配置项类型与配置项类型关联'},
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, comment='配置项类型与配置项关联类型关联ID')
    constraint = sa.Column(sa.Enum(ConfigItemTypeConfigItemTypesConstraint), nullable=False, comment='来源到目标的约束')
    desc = sa.Column(sa.Text, nullable=False, default='', comment='配置项类型与配置项类型关联关联描述')

    ci_type_source_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci_type.id'), nullable=False, comment='来源配置项类型ID')
    ci_type_relation_id = sa.Column(sa.BigInteger, sa.ForeignKey('relation.id'), nullable=True, comment='配置项类型与配置项类型关联关系ID')
    ci_type_target_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci_type.id'), nullable=False, comment='目标配置项类型ID')

    ci_type_source = relationship('ConfigItemTypeModel', foreign_keys=[ci_type_source_id], backref='ci_type_source_ci_type_ci_types')
    ci_type_relation = relationship('RelationModel', foreign_keys=[ci_type_relation_id], backref='ci_type_relation_ci_type_ci_types')
    ci_type_target = relationship('ConfigItemTypeModel', foreign_keys=[ci_type_source_id], backref='ci_type_target_ci_type_ci_types')
