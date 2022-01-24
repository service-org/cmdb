#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy_utils as su

from project.models.base import BaseModel


class ConfigItemTypeGroupModel(BaseModel, su.Timestamp):
    """ 配置项类型分组模型 """
    __tablename__ = 'ci_type_group'
    __table_args__ = (
        # 字典配置必须放最底部
        {'comment': '配置项类型分组'},
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, comment='配置项类型分组ID')
    code = sa.Column(sa.String(32), index=True, unique=True, nullable=False, comment='配置项类型分组编码')
    name = sa.Column(sa.String(64), nullable=False, comment='配置项类型分组名称')
    is_built_in = sa.Column(sa.Boolean, nullable=False, default=False, comment='是否是内置的配置项类型分组?')
    order = sa.Column(sa.BigInteger, nullable=False, default=0, comment='配置项类型分组排序')
