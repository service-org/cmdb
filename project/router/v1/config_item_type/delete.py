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
from project.common.manager.config_item_type import ConfigItemTypeManager

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemType(Endpoint):
    """ 配置项类型接口类 """

    @webserver.api('/apis/v1/ci-type/<int:ci_type_id>/delete', methods=['DELETE'], tags=['ci_type'])
    def delete(
            self, service: Service, request: Request,
            ci_type_id: int = params.Path(Required, description='配置项类型ID')
    ) -> None:
        """ 删除配置项类型

        @param service: 服务对象
        @param request: 请求对象
        @param ci_type_id: 配置项类型id
        @return: None
        """
        ci_type_id = request.path_group_dict['ci_type_id']
        with safe_transaction(service.orm, commit=True) as session:
            ci_type_manager = ConfigItemTypeManager(service, session=session)
            ci_type_manager.delete_by_id(ci_type_id)
