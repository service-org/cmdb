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
from project.common.manager.relation import RelationManager
from service_sqlalchemy.core.shortcuts import safe_transaction
from service_webserver.core.openapi3.generate.depent import params

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class Relation(Endpoint):
    """ 关联关系接口类 """

    @webserver.api('/apis/v1/relation/<int:relation_id>/delete', methods=['DELETE'], tags=['relation'])
    def delete(
            self, service: Service, request: Request,
            relation_id: int = params.Path(Required, description='关联关系ID')
    ) -> None:
        """ 删除关联关系

        @param service: 服务对象
        @param request: 请求对象
        @param relation_id: 关联关系ID
        @return: None
        """
        relation_id = request.path_group_dict['relation_id']
        with safe_transaction(service.orm, commit=True) as session:
            relation_manager = RelationManager(service, session=session)
            relation_manager.delete_by_id(relation_id)
