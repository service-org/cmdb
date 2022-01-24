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
from project.common.manager.relation import RelationManager
from project.schema.v1.relation.create import RelationSchema
from service_sqlalchemy.core.shortcuts import safe_transaction
from service_webserver.core.openapi3.generate.depent import params
from project.schema.v1.relation.create import CreateRelationParams

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class Relation(Endpoint):
    """ 关联类型接口类 """

    @webserver.api('/apis/v1/relation/create', methods=['POST'], tags=['relation'])
    def create(
            self, service: Service, request: Request,
            body: CreateRelationParams = params.Body(Required, description='请求体')
    ) -> t.Dict[t.Text, t.Any]:
        """ 创建关联关系

        @param service: 服务对象
        @param request: 请求对象
        @param body: 请求体内容
        @return: t.Dict[t.Text, t.Any]
        """
        data = request.json or {}
        params = CreateRelationParams(**data)
        validated_data = params.dict(exclude_unset=True)
        with safe_transaction(service.orm, commit=False) as session:
            relation_manager = RelationManager(service, session=session)
            relation_inst = relation_manager.create(validated_data)
            relation_json = RelationSchema.from_orm(relation_inst).json()
            return cjson.loads(relation_json)
