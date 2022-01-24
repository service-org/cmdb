#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy_utils as su

from sqlalchemy.orm import relationship
from project.models.base import BaseModel


class ConfigItemModel(BaseModel, su.Timestamp):
    """ 配置项模型 """
    __tablename__ = 'ci'
    __table_args__ = (
        # 字典配置必须放最底部
        {'comment': '配置项'},
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, comment='配置项ID')

    ci_type_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci_type.id'), nullable=False, comment='配置项类型ID')

    ci_type = relationship('ConfigItemTypeModel', foreign_keys=[ci_type_id], backref='ci_type_cis')
