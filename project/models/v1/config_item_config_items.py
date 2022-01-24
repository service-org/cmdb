#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy_utils as su

from sqlalchemy.orm import relationship
from project.models.base import BaseModel


class ConfigItemConfigItemsModel(BaseModel, su.Timestamp):
    """ 配置项与配置项关联模型 """
    __tablename__ = 'ci_cis'
    __table_args__ = (
        # 字典配置必须放最底部
        {'comment': '配置项与配置项关联'},
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, comment='配置项与配置项关联ID')

    ci_source_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci.id'), nullable=True, comment='来源配置项ID')
    ci_relation_id = sa.Column(sa.BigInteger, sa.ForeignKey('relation.id'), nullable=True, comment='配置项与配合项关系ID')
    ci_target_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci.id'), nullable=True, comment='目标配置项ID')

    ci_source = relationship('ConfigItemModel', foreign_keys=[ci_source_id], backref='ci_source_ci_cis')
    ci_relation = relationship('RelationModel', foreign_keys=[ci_relation_id], backref='ci_relation_ci_cis')
    ci_target = relationship('ConfigItemModel', foreign_keys=[ci_target_id], backref='ci_target_ci_cis')
