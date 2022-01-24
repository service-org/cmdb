#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from collections import namedtuple
from project.service import Service
from pydantic.fields import Required
from sqlalchemy.orm.query import Query
from service_green.core.green import cjson
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.entrypoints import webserver
from project.models.v1.config_item import ConfigItemModel
from service_sqlalchemy.core.client import SQLAlchemyClient
from service_sqlalchemy.core.shortcuts import safe_transaction
from project.common.manager.config_item import ConfigItemManager
from service_webserver.core.openapi3.generate.depent import params
from project.schema.v1.config_item.getall import GetallConfigItemParams
from project.common.manager.config_item_type import ConfigItemTypeManager
from project.schema.v1.config_item_vlaue import ci_value_getall_schema_mapping
from project.common.manager.config_item_vlaue import ConfigItemVlaueProxyManager
from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeModel

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItem(Endpoint):
    """ 配置项接口类 """

    @staticmethod
    def get_all_ci_type_attributes_by_ci_type_id(
            service: Service,
            session: SQLAlchemyClient,
            ci_type_id: int
    ) -> Query:
        """ 根据配置项类型id获取所有配置项类型属性

        @param service: 服务对象
        @param session: 会话对象
        @param ci_type_id: 配置项类型ID
        @return: Query
        """
        ci_type_manager = ConfigItemTypeManager(service, session=session)
        query_columns = [ConfigItemTypeAttributeModel.id,
                         ConfigItemTypeAttributeModel.code,
                         ConfigItemTypeAttributeModel.value_type
                         ]
        return ci_type_manager.get_all_ci_type_attributes_by_id(
            ci_type_id, query_columns=query_columns
        )

    @staticmethod
    def get_all_ci_values(
            service: Service,
            session: SQLAlchemyClient,
            ci_id_list: t.List[int],
            ci_value_type_set: t.Set[t.Text]
    ) -> t.Generator[t.Dict[t.Text, t.Any]]:
        """ 根据配置项id列表获取所有配置项值

        @param service: 服务对象
        @param session: 会话对象
        @param ci_id_list: 配置项id列表
        @param ci_value_type_set: 配置项值类型集合
        @return: t.Dict[t.Text, t.Any]
        """
        ci_value_manager = ConfigItemVlaueProxyManager(service, session=session)
        for value_type in ci_value_type_set:
            value_schema = ci_value_getall_schema_mapping[value_type]
            ci_values = ci_value_manager.batch_get_by_ci_id(ci_id_list, value_type).all()
            for ci_value in cjson.loads(value_schema(__root__=ci_values).json()): yield ci_value

    @webserver.api('/apis/v1/ci/getall', methods=['GET'], tags=['ci'])
    def getall(
            self, service: Service, request: Request,
            page: int = params.Query(1, ge=1, description='当前页码'),
            ci_type_id: int = params.Query(Required, description='配置项类型ID'),
            page_size: int = params.Query(10, ge=10, le=200, description='分页大小')
    ) -> t.Dict[t.Text, t.Any]:
        """ 获取所有配置项

        @param service: 服务对象
        @param request: 请求对象
        @param page: 当前页码
        @param page_size: 分页大小
        @param ci_type_id: 配置项类型id
        @return: t.Dict[t.Text, t.Any]
        """
        result = {}
        data = request.args.to_dict()
        params = GetallConfigItemParams(**data)
        with safe_transaction(service.orm, commit=False) as session:
            ci_type_attributes = self.get_all_ci_type_attributes_by_ci_type_id(
                service, session=session, ci_type_id=params.ci_type_id
            )
            ci_type_attribute_map, ci_value_type_set = {}, set()
            for ci_type_attribute in ci_type_attributes:
                ci_value_type_set.add(ci_type_attribute.value_type.value)
                ci_type_attribute_map[ci_type_attribute.id] = ci_type_attribute.code
            ci_manager = ConfigItemManager(service, session=session)
            queryset = ci_manager.get_by_ci_type_id(params.ci_type_id, query_columns=[ConfigItemModel.id])
            ci_total = queryset.count()
            queryset = queryset.slice((params.page - 1) * params.page_size, params.page * params.page_size)
            ci_id_list = [ins.id for ins in queryset]
            ci_values = self.get_all_ci_values(
                service, session=session, ci_id_list=ci_id_list, ci_value_type_set=ci_value_type_set
            )
            for ci_value in ci_values:
                ci_id = ci_value['ci_id']
                ci_type_attribute_id = ci_value['ci_type_attribute_id']
                code = ci_type_attribute_map[ci_type_attribute_id]
                value = ci_value['value']
                result.setdefault(ci_id, dict.fromkeys(ci_type_attribute_map.values())).update({code: value})
            return {'total': ci_total, 'items': [{'id': k} | v for k, v in result.items()]}
