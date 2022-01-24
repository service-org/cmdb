#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from project.service import Service
from pydantic.fields import Required
from project.models.base import BaseModel
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.entrypoints import webserver
from service_sqlalchemy.core.shortcuts import safe_transaction
from service_webserver.core.openapi3.generate.depent import params
from project.common.manager.config_item_type_attribute_group import ConfigItemTypeAttributeGroupManager
from project.schema.v1.config_item_type_attribute_group.getall import GetallConfigItemTypeAttributeGroupParams

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class ConfigItemTypeAttributeGroup(Endpoint):
    """ 配置项类型属性分组接口类 """

    @staticmethod
    def gen_ci_type_group_key(item: BaseModel) -> t.Tuple:
        """ 生成配置项类型属性分组键

        @param item: 实例对象
        @return: t.Tuple
        """
        return (
            ('id', item.id),
            ('code', item.code),
            ('name', item.name),
            ('is_collapse', item.is_collapse),
            ('order', item.order)
        )

    @webserver.api('/apis/v1/ci-type-attribute-group/getall', methods=['GET'], tags=['ci_type_attribute_group'])
    def getall(
            self, service: Service, request: Request,
            ci_type_id: int = params.Query(Required, description='配置项类型id')
    ) -> t.List[t.Dict[t.Text, t.Any]]:
        """ 获取所有配置项类型分组

        @param service: 服务对象
        @param request: 请求对象
        @param ci_type_id: 配置项类型id
        @return: t.List[t.Dict[t.Text, t.Any]]
        """
        result = {}
        data = request.args.to_dict()
        params = GetallConfigItemTypeAttributeGroupParams(**data)
        ci_type_id = params.ci_type_id
        with safe_transaction(service.orm, commit=False) as session:
            ci_type_attribute_group_manager = ConfigItemTypeAttributeGroupManager(service, session=session)
            for item in ci_type_attribute_group_manager.get_all_by_ci_type_id(ci_type_id):
                key = self.gen_ci_type_group_key(item)
                result.setdefault(key, [])
            for item in ci_type_attribute_group_manager.get_all_ci_type_attributes_by_ci_type_id(ci_type_id):
                key = self.gen_ci_type_group_key(item)
                result[key].append({
                    'id': item.ci_type_attribute_id,
                    'code': item.ci_type_attribute_code,
                    'name': item.ci_type_attribute_name,
                    'tips': item.ci_type_attribute_tips,
                    'order': item.ci_type_attribute_order,
                    'value_type': item.ci_type_attribute_value_type.value,
                    'value_is_editable': item.ci_type_attribute_value_is_editable,
                    'value_is_required': item.ci_type_attribute_value_is_required,
                    'value_is_password': item.ci_type_attribute_value_is_password,
                    'value_is_url_link': item.ci_type_attribute_value_is_url_link,
                    'value_re_patterns': item.ci_type_attribute_value_re_patterns,
                    'value_ge_limit_nu': item.ci_type_attribute_value_ge_limit_nu,
                    'value_le_limit_nu': item.ci_type_attribute_value_le_limit_nu
                })
            return [dict(k) | {'ci_type_attributes': result[k]} for k in result]
