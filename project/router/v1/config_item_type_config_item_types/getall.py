#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from project.service import Service
from service_green.core.green import cjson
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.entrypoints import webserver
from service_sqlalchemy.core.shortcuts import safe_transaction
from project.common.manager.config_item_type_config_item_types import ConfigItemTypeConfigItemTypesManager
from project.schema.v1.config_item_type_config_item_types.getall import ListConfigItemTypeConfigItemTypesSchema

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemTypeConfigItemTypes(Endpoint):
    """ 配置项类型与配置项类型关联关系接口类 """

    @webserver.api('/apis/v1/ci-type-ci-types/getall', methods=['GET'], tags=['ci_type_ci_types'])
    def getall(
            self, service: Service, request: Request,
    ) -> t.List[t.Dict[t.Text, t.Any]]:
        """ 获取所有配置项类型与配置项类型关联关系

        @param service: 服务对象
        @param request: 请求对象
        @return: t.List[t.Dict[t.Text, t.Any]]
        """
        with safe_transaction(service.orm, commit=False) as session:
            ci_type_ci_types_manager = ConfigItemTypeConfigItemTypesManager(service, session=session)
            ci_type_ci_types_objs = ci_type_ci_types_manager.get_all().all()
            ci_type_ci_types_json = ListConfigItemTypeConfigItemTypesSchema(__root__=ci_type_ci_types_objs).json()
            return cjson.loads(ci_type_ci_types_json)
