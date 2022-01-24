#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy_utils as su

from enum import Enum
from project.models.base import BaseModel


class RelationDirection(Enum):
    """ 关系方向 """
    # source ->  target
    STOT = 'stot'
    # target ->  source
    TTOS = 'ttos'
    # source <-> target
    BOTH = 'both'
    # source     target
    NONE = 'none'


class RelationModel(BaseModel, su.Timestamp):
    """ 关系模型 """
    __tablename__ = 'relation'
    __table_args__ = (
        # 字典配置必须放最底部
        {'comment': '关系'},
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, comment='关系类型ID')
    code = sa.Column(sa.String(32), index=True, unique=True, nullable=False, comment='关系类型编码')
    name = sa.Column(sa.String(64), nullable=False, comment='关系类型名称')
    is_built_in = sa.Column(sa.Boolean, nullable=False, default=False, comment='是否是内置的关系类型?')
    source_to_target_desc = sa.Column(sa.String(64), nullable=False, comment='源头到目标关系类型描述')
    target_to_source_desc = sa.Column(sa.String(64), nullable=False, comment='目标到源头关系类型描述')
    direction = sa.Column(sa.Enum(RelationDirection), nullable=False, default=RelationDirection.STOT, comment='关系方向')
