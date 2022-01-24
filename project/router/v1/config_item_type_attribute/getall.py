#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from pydantic import Required
from project.service import Service
from service_green.core.green import cjson
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.entrypoints import webserver
from service_sqlalchemy.core.shortcuts import safe_transaction
from service_webserver.core.openapi3.generate.depent import params
from project.common.manager.config_item_type_attribute import ConfigItemTypeAttributeManager
from project.schema.v1.config_item_type_attribute.getall import ListConfigItemTypeAttributeSchema
from project.schema.v1.config_item_type_attribute.getall import GetallConfigItemTypeAttributeParams

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemTypeAttribute(Endpoint):
    """ 配置项类型属性接口类 """

    @webserver.api('/apis/v1/ci-type-attribute/getall', methods=['GET'], tags=['ci_type_attribute'])
    def getall(
            self, service: Service, request: Request,
            ci_type_attribute_group_id: int = params.Query(Required, description='配置项类型属性分组id')
    ) -> t.List[t.Dict[t.Text, t.Any]]:
        """ 获取所有配置项类型

        @param service: 服务对象
        @param request: 请求对象
        @param ci_type_attribute_group_id: 配置项类型属性分组id
        @return: t.List[t.Dict[t.Text, t.Any]]
        """
        data = request.args.to_dict()
        params = GetallConfigItemTypeAttributeParams(**data)
        ci_type_attribute_group_id = params.ci_type_attribute_group_id
        with safe_transaction(service.orm, commit=False) as session:
            ci_type_attribute_manager = ConfigItemTypeAttributeManager(service, session=session)
            ci_type_attribute_objs = ci_type_attribute_manager.get_by_ci_type_attribute_group_id(ci_type_attribute_group_id).all()
            ci_type_json = ListConfigItemTypeAttributeSchema(__root__=ci_type_attribute_objs).json()
            return cjson.loads(ci_type_json)
