#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from logging import getLogger
from project.service import Service
from service_sqlalchemy.core.client import SQLAlchemyClient

logger = getLogger(__name__)


class ConfigItemTypeUniqueIndexManager(object):
    """ 配置项类型唯一索引管理器 """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ 初始化实例

        @param service: 服务对象
        @param session: 会话对象
        """
        self.service = service
        self.session = session
