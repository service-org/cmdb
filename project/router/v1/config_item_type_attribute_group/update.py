#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from logging import getLogger
from project.service import Service
from pydantic.fields import Required
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.entrypoints import webserver
from service_sqlalchemy.core.shortcuts import safe_transaction
from service_webserver.core.openapi3.generate.depent import params
from project.common.manager.config_item_type_attribute_group import ConfigItemTypeAttributeGroupManager
from project.schema.v1.config_item_type_attribute_group.update import UpdateConfigItemTypeAttributeGroupParams

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemTypeAttributeGroup(Endpoint):
    """ 配置项类型属性分组接口类 """

    @webserver.api('/apis/v1/ci-type-attribute-group/<int:ci_type_attribute_group_id>/update', methods=['PATCH'], tags=['ci_type_attribute_group'])
    def update(
            self, service: Service, request: Request,
            ci_type_attribute_group_id: int = params.Path(Required, description='配置项类型属性分组ID'),
            body: UpdateConfigItemTypeAttributeGroupParams = params.Body(Required, description='请求体')
    ) -> None:
        """ 更新配置项类型属性分组

        @param service: 服务对象
        @param request: 请求对象
        @param ci_type_attribute_group_id: 配置项类型属性分组ID
        @param body: 请求体内容
        @return: None
        """
        data = request.json or {}
        ci_type_attribute_group_id = request.path_group_dict['ci_type_attribute_group_id']
        params = UpdateConfigItemTypeAttributeGroupParams(**data)
        validated_data = params.dict(exclude_unset=True)
        with safe_transaction(service.orm, commit=True) as session:
            ci_type_attribute_group_manager = ConfigItemTypeAttributeGroupManager(service, session=session)
            ci_type_attribute_group_manager.update_by_id(ci_type_attribute_group_id, validated_data=validated_data)
