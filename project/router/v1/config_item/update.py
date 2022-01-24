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
from project.common.manager.config_item import ConfigItemManager
from service_webserver.core.openapi3.generate.depent import params
from project.schema.v1.config_item.update import UpdateConfigItemParams

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItem(Endpoint):
    """ 配置项接口类 """

    @webserver.api('/apis/v1/ci/<int:ci_id>/update', methods=['PATCH'], tags=['ci'])
    def update(
            self, service: Service, request: Request,
            ci_id: int = params.Path(Required, description='配置项ID'),
            body: UpdateConfigItemParams = params.Body(Required, description='请求体')
    ) -> None:
        """ 更新配置项

        @param service: 服务对象
        @param request: 请求对象
        @param ci_id: 配置项id
        @param body: 请求体内容
        @return: None
        """
        data = request.json or {}
        ci_id = request.path_group_dict['ci_id']
        params = UpdateConfigItemParams(**data)
        validated_data = params.dict(exclude_unset=True)
        with safe_transaction(service.orm, commit=True) as session:
            ci_manager = ConfigItemManager(service, session=session)
            ci_manager.update_by_id(ci_id, validated_data)
