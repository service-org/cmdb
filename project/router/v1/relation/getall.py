#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from project.service import Service
from service_green.core.green import cjson
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.entrypoints import webserver
from project.common.manager.relation import RelationManager
from service_sqlalchemy.core.shortcuts import safe_transaction
from service_webserver.core.openapi3.generate.depent import params
from project.schema.v1.relation.getall import GetallRelationSchema

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class Relation(Endpoint):
    """ 关联关系接口类 """

    @webserver.api('/apis/v1/relation/getall', methods=['GET'], tags=['relation'])
    def getall(
            self, service: Service, request: Request,
            page: int = params.Query(1, ge=1, description='当前页码'),
            page_size: int = params.Query(10, ge=10, le=200, description='分页大小')
    ) -> t.Dict[t.Text, t.Any]:
        """ 获取所有关联关系

        @param service: 服务对象
        @param request: 请求对象
        @param page: 当前页码
        @param page_size: 分页大小
        @return: t.Dict[t.Text, t.Any]
        """
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        with safe_transaction(service.orm, commit=False) as session:
            relation_manager = RelationManager(service, session=session)
            relation_objs = relation_manager.get_all()
            total = relation_objs.count()
            items = relation_objs.slice((page - 1) * page_size, page * page_size).all()
            relation_json = GetallRelationSchema(total=total, items=items).json()
            return cjson.loads(relation_json)
