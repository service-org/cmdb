#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy_utils as su

from sqlalchemy.orm import relationship
from project.models.base import BaseModel


class ConfigItemTypeModel(BaseModel, su.Timestamp):
    """ 配置项类型模型 """
    __tablename__ = 'ci_type'
    __table_args__ = (
        # 字典配置必须放最底部
        {'comment': '配置项类型'},
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, comment='配置项类型ID')
    code = sa.Column(sa.String(32), index=True, unique=True, comment='配置项类型编码')
    name = sa.Column(sa.String(64), nullable=False, comment='配置项类型名称')
    order = sa.Column(sa.BigInteger, nullable=False, default=0, comment='配置项类型排序')
    is_built_in = sa.Column(sa.Boolean, nullable=False, default=False, comment='是否是内置的配置项类型?')
    is_disabled = sa.Column(sa.Boolean, nullable=False, default=False, comment='是否是停用的配置项类型?')
    is_not_show = sa.Column(sa.Boolean, nullable=False, default=False, comment='是否要不显示配置项类型?')
    icon = sa.Column(sa.String(32), nullable=False, default='', comment='配置项类型图标')
    desc = sa.Column(sa.Text, nullable=False, default='', comment='配置项类型描述')

    ci_type_group_id = sa.Column(sa.BigInteger, sa.ForeignKey('ci_type_group.id'), nullable=False, comment='配置项类型分组ID')

    ci_type_group = relationship('ConfigItemTypeGroupModel', foreign_keys=[ci_type_group_id], backref='ci_type_group_ci_types')
