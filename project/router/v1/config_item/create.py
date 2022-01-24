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
from project.common.manager.config_item import ConfigItemManager
from project.schema.v1.config_item.create import ConfigItemSchema
from service_webserver.core.openapi3.generate.depent import params
from project.schema.v1.config_item.create import CreateConfigItemParams


router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItem(Endpoint):
    """ 配置项接口类 """

    @webserver.api('/apis/v1/ci/create', methods=['POST'], tags=['ci'])
    def create(
            self, service: Service, request: Request,
            body: CreateConfigItemParams = params.Body(Required, description='请求体')
    ) -> t.Dict[t.Text, t.Any]:
        """ 创建配置项

        @param service: 服务对象
        @param request: 请求对象
        @param body: 请求体内容
        @return: t.Dict[t.Text, t.Any]
        """
        data = request.json or {}
        params = CreateConfigItemParams(**data)
        validated_data = params.dict(exclude_unset=True)
        with safe_transaction(service.orm, commit=False) as session:
            ci_manager = ConfigItemManager(service, session=session)
            ci_inst = ci_manager.create(validated_data)
            ci_json = ConfigItemSchema.from_orm(ci_inst).json()
            return cjson.loads(ci_json)
