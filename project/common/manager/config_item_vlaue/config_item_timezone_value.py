#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from project.service import Service
from sqlalchemy.orm.query import Query
from service_sqlalchemy.core.client import SQLAlchemyClient
from project.models.v1.config_item_vlaue.config_item_timezone_value import ConfigItemTimezoneValueModel
from project.exception.config_item_vlaue.config_item_timezone_value import NotFoundConfigItemTimezoneValueError

logger = getLogger(__name__)


class ConfigItemTimezoneValueManager(object):
    """ 配置项时区值管理器 """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ 初始化实例

        @param service: 服务对象
        @param session: 会话对象
        """
        self.service = service
        self.session = session

    def batch_get_by_ci_id(self, ci_id_list: t.List[int], raise_error: t.Optional[bool] = False) -> Query:
        """ 根据配置项id列表获取配置项时区值

        @param ci_id_list: 配置项id列表
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        ci_timezone_values = self.session.query(ConfigItemTimezoneValueModel).filter(ConfigItemTimezoneValueModel.ci_id.in_(ci_id_list))
        if not ci_timezone_values and raise_error: raise NotFoundConfigItemTimezoneValueError(f'未找到配置项时区值{ci_id_list}')
        return ci_timezone_values

    def get_by_ci_id(self, ci_id_list: int, raise_error: t.Optional[bool] = False) -> Query:
        """ 根据配置项id获取配置项时区值

        @param ci_id_list: 配置项id
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        return self.batch_get_by_ci_id([ci_id_list], raise_error=raise_error)

    def batch_delete_by_ci_id(self, ci_id_list: t.List[int]) -> None:
        """ 根据配置项id列表批量删除配置项时区值

        @param ci_id_list: 配置项id列表
        @return: None
        """
        ci_timezone_values = self.batch_get_by_ci_id(ci_id_list, raise_error=False)
        ci_timezone_values.delete(synchronize_session=False)

    def delete_by_ci_id(self, ci_id: int) -> None:
        """ 根据配置项id删除配置项时区值

        @param ci_id: 配置项id
        @return: None
        """
        ci_timezone_values = self.get_by_ci_id(ci_id, raise_error=True)
        ci_timezone_values.delete(synchronize_session=False)
