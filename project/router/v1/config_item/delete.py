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

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItem(Endpoint):
    """ 配置项接口类 """

    @webserver.api('/apis/v1/ci/<int:ci_id>/delete', methods=['DELETE'], tags=['ci'])
    def delete(
            self, service: Service, request: Request,
            ci_id: int = params.Path(Required, description='配置项ID')
    ) -> None:
        """ 删除配置项

        @param service: 服务对象
        @param request: 请求对象
        @param ci_id: 配置项id
        @return: None
        """
        ci_id = request.path_group_dict['ci_id']
        with safe_transaction(service.orm, commit=True) as session:
            ci_manager = ConfigItemManager(service, session=session)
            ci_manager.delete_by_id(ci_id)
