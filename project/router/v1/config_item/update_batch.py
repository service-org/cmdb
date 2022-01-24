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
from project.schema.v1.config_item.update_batch import UpdateBatchConfigItemParams

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItem(Endpoint):
    """ 配置项接口类 """

    @webserver.api('/apis/v1/ci/update-batch', methods=['PATCH'], tags=['ci'])
    def update_batch(
            self, service: Service, request: Request,
            body: UpdateBatchConfigItemParams = params.Body(Required, description='请求体')
    ) -> None:
        """ 批量更新配置项

        @param service: 服务对象
        @param request: 请求对象
        @param body: 请求体内容
        @return: None
        """
        data = request.json or {}
        params = UpdateBatchConfigItemParams(**data)
        validated_data = params.dict(exclude_unset=True)['ci_values']
        with safe_transaction(service.orm, commit=True) as session:
            ci_manager = ConfigItemManager(service, session=session)
            ci_manager.batch_update_by_id(params.ci_id_list, validated_data)
