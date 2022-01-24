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
from project.common.manager.config_item_type_group import ConfigItemTypeGroupManager
from project.schema.v1.config_item_type_group.create import ConfigItemTypeGroupSchema
from project.schema.v1.config_item_type_group.create import CreateConfigItemTypeGroupParams

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemTypeGroup(Endpoint):
    """ 配置项类型分组接口类 """

    @webserver.api('/apis/v1/ci-type-group/create', methods=['POST'], tags=['ci_type_group'])
    def create(
            self, service: Service, request: Request,
            body: CreateConfigItemTypeGroupParams = params.Body(Required, description='请求体')
    ) -> t.Dict[t.Text, t.Any]:
        """ 创建配置项类型分组

        @param service: 服务对象
        @param request: 请求对象
        @param body: 请求体内容
        @return: t.Dict[t.Text, t.Any]
        """
        data = request.json or {}
        params = CreateConfigItemTypeGroupParams(**data)
        validated_data = params.dict(exclude_unset=True)
        with safe_transaction(service.orm, commit=False) as session:
            ci_type_group_manager = ConfigItemTypeGroupManager(service, session=session)
            ci_type_group_inst = ci_type_group_manager.create(validated_data)
            ci_type_group_json = ConfigItemTypeGroupSchema.from_orm(ci_type_group_inst).json()
            return cjson.loads(ci_type_group_json)
