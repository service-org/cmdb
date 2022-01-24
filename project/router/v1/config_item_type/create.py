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
from project.common.manager.config_item_type import ConfigItemTypeManager
from project.schema.v1.config_item_type.create import ConfigItemTypeSchema
from project.schema.v1.config_item_type.create import CreateConfigItemTypeParams


router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemType(Endpoint):
    """ 配置项类型接口类 """

    @webserver.api('/apis/v1/ci-type/create', methods=['POST'], tags=['ci_type'])
    def create(
            self, service: Service, request: Request,
            body: CreateConfigItemTypeParams = params.Body(Required, description='请求体')
    ) -> t.Dict[t.Text, t.Any]:
        """ 创建配置项类型

        @param service: 服务对象
        @param request: 请求对象
        @param body: 请求体内容
        @return: t.Dict[t.Text, t.Any]
        """
        data = request.json or {}
        params = CreateConfigItemTypeParams(**data)
        validated_data = params.dict(exclude_unset=True)
        with safe_transaction(service.orm, commit=False) as session:
            ci_type_manager = ConfigItemTypeManager(service, session=session)
            ci_type_inst = ci_type_manager.create(validated_data)
            ci_type_json = ConfigItemTypeSchema.from_orm(ci_type_inst).json()
            return cjson.loads(ci_type_json)
