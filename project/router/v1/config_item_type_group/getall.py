#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from project.service import Service
from project.models.base import BaseModel
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.entrypoints import webserver
from service_sqlalchemy.core.shortcuts import safe_transaction
from project.models.v1.config_item_type_group import ConfigItemTypeGroupModel
from project.common.manager.config_item_type_group import ConfigItemTypeGroupManager

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemTypeGroup(Endpoint):
    """ 配置项类型分组接口类 """

    @staticmethod
    def gen_ci_type_group_key(item: BaseModel) -> t.Tuple:
        """ 生成配置项类型分组键

        @param item: 实例对象
        @return: t.Tuple
        """
        return (
            ('id', item.id),
            ('code', item.code),
            ('name', item.name),
            ('is_built_in', item.is_built_in),
            ('order', item.order)
        )

    @webserver.api('/apis/v1/ci-type-group/getall', methods=['GET'], tags=['ci_type_group'])
    def getall(
            self, service: Service, request: Request
    ) -> t.List[t.Dict[t.Text, t.Any]]:
        """ 获取所有配置项类型分组

        @param service: 服务对象
        @param request: 请求对象
        @return: t.List[t.Dict[t.Text, t.Any]]
        """
        result = {}
        with safe_transaction(service.orm, commit=False) as session:
            ci_type_group_manager = ConfigItemTypeGroupManager(service, session=session)
            query_columns = [
                ConfigItemTypeGroupModel.id,
                ConfigItemTypeGroupModel.code,
                ConfigItemTypeGroupModel.name,
                ConfigItemTypeGroupModel.is_built_in,
                ConfigItemTypeGroupModel.order
            ]
            for item in ci_type_group_manager.get_all(query_columns):
                key = self.gen_ci_type_group_key(item)
                result.setdefault(key, [])
            for item in ci_type_group_manager.get_all_ci_types():
                key = self.gen_ci_type_group_key(item)
                result[key].append({
                    'id': item.ci_type_id,
                    'code': item.ci_type_code,
                    'name': item.ci_type_name,
                    'icon': item.ci_type_icon,
                    'desc': item.ci_type_desc,
                    'is_built_in': item.ci_type_is_built_in,
                    'is_disabled': item.ci_type_is_disabled,
                    'is_not_show': item.ci_type_is_not_show,
                    'order': item.ci_type_order
                })
            return [dict(k) | {'ci_types': result[k]} for k in result]
