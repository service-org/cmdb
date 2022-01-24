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
from project.common.manager.config_item_type_attribute import ConfigItemTypeAttributeManager
from project.schema.v1.config_item_type_attribute.create import ConfigItemTypeAttributeSchema
from project.schema.v1.config_item_type_attribute.create import CreateConfigItemTypeAttributeParams

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemTypeAttribute(Endpoint):
    """ 配置项类型属性接口类 """

    @webserver.api('/apis/v1/ci-type-attribute/create', methods=['POST'], tags=['ci_type_attribute'])
    def create(
            self, service: Service, request: Request,
            body: CreateConfigItemTypeAttributeParams = params.Body(Required, description='请求体')
    ) -> t.Dict[t.Text, t.Any]:
        """ 创建配置项类型

        @param service: 服务对象
        @param request: 请求对象
        @param body: 请求体内容
        @return: t.Dict[t.Text, t.Any]
        """
        data = request.json or {}
        params = CreateConfigItemTypeAttributeParams(**data)
        validated_data = params.dict(exclude_unset=True)
        with safe_transaction(service.orm, commit=False) as session:
            ci_type_attribute_manager = ConfigItemTypeAttributeManager(service, session=session)
            ci_type_attribute_inst = ci_type_attribute_manager.create(validated_data)
            ci_type_attribute_json = ConfigItemTypeAttributeSchema.from_orm(ci_type_attribute_inst).json()
            return cjson.loads(ci_type_attribute_json)
