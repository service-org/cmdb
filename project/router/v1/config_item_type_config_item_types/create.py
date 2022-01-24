#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from project.service import Service
from pydantic.fields import Required
from service_green.core.green import cjson
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.entrypoints import webserver
from service_sqlalchemy.core.shortcuts import safe_transaction
from service_webserver.core.openapi3.generate.depent import params
from project.common.manager.config_item_type_config_item_types import ConfigItemTypeConfigItemTypesManager
from project.schema.v1.config_item_type_config_item_types.create import ConfigItemTypeConfigItemTypesSchema
from project.schema.v1.config_item_type_config_item_types.create import CreateConfigItemTypeConfigItemTypesParams

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemTypeConfigItemTypes(Endpoint):
    """ 配置项类型与配置项类型关联关系接口类 """

    @webserver.api('/apis/v1/ci-type-ci-types/create', methods=['POST'], tags=['ci_type_ci_types'])
    def create(
            self, service: Service, request: Request,
            body: CreateConfigItemTypeConfigItemTypesParams = params.Body(Required, description='请求体')
    ) -> t.Dict[t.Text, t.Any]:
        """ 创建配置项类型与配置项类型关联关系

        @param service: 服务对象
        @param request: 请求对象
        @param body: 请求体内容
        @return: t.Dict[t.Text, t.Any]
        """
        data = request.json or {}
        params = CreateConfigItemTypeConfigItemTypesParams(**data)
        validated_data = params.dict(exclude_unset=True)
        with safe_transaction(service.orm, commit=False) as session:
            ci_type_ci_types_manager = ConfigItemTypeConfigItemTypesManager(service, session=session)
            ci_type_ci_type_inst = ci_type_ci_types_manager.create(validated_data)
            ci_type_ci_type_json = ConfigItemTypeConfigItemTypesSchema.from_orm(ci_type_ci_type_inst).json()
            return cjson.loads(ci_type_ci_type_json)
