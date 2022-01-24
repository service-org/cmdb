#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from project.service import Service
from sqlalchemy.orm.query import Query
from service_sqlalchemy.core.client import SQLAlchemyClient
from project.models.v1.config_item_type import ConfigItemTypeModel
from project.exception.config_item_type_attribute_group.delete import (
    NotAllowedDeleteGroupThatHasConfigItemTypeAttributeError
)
from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeModel
from project.models.v1.config_item_type_attribute_group import ConfigItemTypeAttributeGroupModel
from project.exception.config_item_type_attribute_group import NotFoundConfigItemTypeAttributeGroupError


class ConfigItemTypeAttributeGroupManager(object):
    """ 配置项类型属性分组管理器 """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ 初始化实例

        @param service: 服务对象
        @param session: 会话对象
        """
        self.service = service
        self.session = session

    def check_create_duplication(self, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 检查创建时是否存在重复配置项类型属性分组

        @param validated_data: 验证后的数据
        @return: None
        """
        code = validated_data.get('code', '')
        name = validated_data.get('name', '')
        ci_type_id = validated_data.get('ci_type_id', 0)
        query_columns = [ConfigItemTypeAttributeGroupModel.id]
        filter_conditions = [ConfigItemTypeAttributeGroupModel.ci_type_id == ci_type_id,
                             ConfigItemTypeAttributeGroupModel.code == code]
        if not self.session.query(*query_columns).filter(*filter_conditions).first(): return
        raise NotFoundConfigItemTypeAttributeGroupError(f'数据唯一性校验失败，{name}({code}) 重复')

    def create(self, validated_data: t.Dict[t.Text, t.Any]) -> ConfigItemTypeAttributeGroupModel:
        """ 创建指定配置项类型属性分组

        @param validated_data: 验证后的数据
        @return: ConfigItemTypeAttributeGroupModel
        """
        self.check_create_duplication(
            validated_data
        )
        instance = ConfigItemTypeAttributeGroupModel(
            **validated_data
        )
        self.session.add(instance)
        self.session.commit()

        return instance

    def batch_get_by_id(
            self,
            ci_type_attribute_group_id_list: t.List[int],
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False) -> Query:
        """ 根据配置类型属性分组id列表获取配置类型属性分组

        @param ci_type_attribute_group_id_list: 配置项类型属性分组id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeAttributeGroupModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        query_columns = [ConfigItemTypeAttributeGroupModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemTypeAttributeGroupModel.id.in_(ci_type_attribute_group_id_list)]
        queryset = self.session.query(*query_columns).filter(*filter_conditions)
        if queryset.first() or not raise_error: return queryset
        raise NotFoundConfigItemTypeAttributeGroupError(f'未找到配置项类型属性分组{ci_type_attribute_group_id_list}')

    def get_by_id(
            self,
            ci_type_attribute_group_id: int,
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False) -> Query:
        """ 根据配置项类型属性分组id获取配置项类型属性分组

        @param ci_type_attribute_group_id: 配置项类型属性分组id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeAttributeGroupModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        return self.batch_get_by_id([ci_type_attribute_group_id], query_columns=query_columns, raise_error=raise_error)

    def batch_update_by_id(
            self,
            ci_type_attribute_group_id_list: t.List[int],
            validated_data: t.Dict[t.Text, t.Any]
    ) -> None:
        """ 根据配置项类型属性分组id列表批量更新配置项类型属性分组

        @param ci_type_attribute_group_id_list: 配置项类型属性分组id列表
        @param validated_data: 验证后的数据
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_attribute_group_id_list, raise_error=False)
        queryset.update(validated_data)

    def update_by_id(self, ci_type_attribute_group_id: int, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置项类型属性分组id更新配置项类型属性分组

        @param ci_type_attribute_group_id: 配置项类型属性分组id
        @param validated_data: 验证后的数据
        @return: None
        """
        instance = self.get_by_id(
            ci_type_attribute_group_id, raise_error=True
        ).first()
        for k, v in validated_data.items():
            setattr(instance, k, v)

    def batch_delete_by_id(self, ci_type_attribute_group_id_list: t.List[int]) -> None:
        """ 根据配置项类型属性分组id列表批量删除配置项类型属性分组

        @param ci_type_attribute_group_id_list: 配置项类型属性分组id列表
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_attribute_group_id_list, raise_error=False)
        queryset.delete(synchronize_session=False)

    def delete_by_id(self, ci_type_attribute_group_id: int) -> None:
        """ 根据配置项类型属性分组id删除配置项类型属性分组

        @param ci_type_attribute_group_id: 配置项类型属性分组id
        @return: None
        """
        queryset = self.get_by_id(ci_type_attribute_group_id, raise_error=True)
        instance = queryset.first()
        ci_type_attributes = instance.ci_type_attribute_group_ci_type_attributes
        if not ci_type_attributes: return queryset.delete(synchronize_session=False)
        raise NotAllowedDeleteGroupThatHasConfigItemTypeAttributeError('分组下有配置项类型属性,不允许删除')

    def batch_get_by_ci_type_id(self, ci_type_id_list: t.List[int], query_columns: t.Optional[t.List] = None) -> Query:
        """ 根据配置项类型id列表批量获取配置项类型属性分组

        @param ci_type_id_list: 配置项类型id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeAttributeGroupModel]
        @return: Query
        """
        query_columns = [ConfigItemTypeAttributeGroupModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemTypeAttributeGroupModel.ci_type_id.in_(ci_type_id_list)]
        return self.session.query(*query_columns).filter(*filter_conditions)

    def get_by_ci_type_id(self, ci_type_id: int, query_columns: t.Optional[t.List] = None) -> Query:
        """ 根据配置项类型id获取配置项类型属性分组

        @param ci_type_id: 配置项类型id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeAttributeGroupModel]
        @return: Query
        """
        return self.batch_get_by_ci_type_id([ci_type_id], query_columns=query_columns)

    def batch_delete_by_ci_type_id(self, ci_type_id_list: t.List[int]) -> None:
        """ 根据配置项类型id列表批量删除配置项类型属性分组

        @param ci_type_id_list: 配置项类型id列表
        @return: None
        """
        queryset = self.batch_get_by_ci_type_id(ci_type_id_list)
        queryset.delete(synchronize_session=False)

    def delete_by_ci_type_id(self, ci_type_id: int) -> None:
        """ 根据配置项类型id删除配置项类型属性分组

        @param ci_type_id: 配置项类型id
        @return: None
        """
        self.batch_delete_by_ci_type_id([ci_type_id])

    def get_all_by_ci_type_id(self, ci_type_id: int, query_columns: t.Optional[t.List] = None) -> Query:
        """ 根据配置项类型id获取所有配置项类型属性分组

        @param ci_type_id: 配置项类型id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeAttributeGroupModel]
        @return: Query
        """
        query_columns = [ConfigItemTypeAttributeGroupModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemTypeAttributeGroupModel.ci_type_id == ci_type_id]
        return self.session.query(*query_columns).filter(*filter_conditions)

    def get_all_ci_type_attributes_by_ci_type_id(self, ci_type_id: int) -> Query:
        """ 根据配置类型id获取配置类型分组下的所有配置类型属性

        @param ci_type_id: 配置类型属性id
        @return: Query
        """
        return self.session.query(
            ConfigItemTypeAttributeModel
        ).join(
            ConfigItemTypeAttributeGroupModel,
            ConfigItemTypeAttributeGroupModel.id == ConfigItemTypeAttributeModel.ci_type_attribute_group_id
        ).join(
            ConfigItemTypeModel,
            ConfigItemTypeModel.id == ConfigItemTypeAttributeGroupModel.ci_type_id
        ).filter(
            ConfigItemTypeAttributeGroupModel.ci_type_id == ci_type_id
        ).with_entities(
            ConfigItemTypeAttributeGroupModel.id,
            ConfigItemTypeAttributeGroupModel.code,
            ConfigItemTypeAttributeGroupModel.name,
            ConfigItemTypeAttributeGroupModel.order,
            ConfigItemTypeAttributeGroupModel.is_collapse,
            ConfigItemTypeAttributeModel.id.label('ci_type_attribute_id'),
            ConfigItemTypeAttributeModel.code.label('ci_type_attribute_code'),
            ConfigItemTypeAttributeModel.name.label('ci_type_attribute_name'),
            ConfigItemTypeAttributeModel.tips.label('ci_type_attribute_tips'),
            ConfigItemTypeAttributeModel.order.label('ci_type_attribute_order'),
            ConfigItemTypeAttributeModel.value_type.label('ci_type_attribute_value_type'),
            ConfigItemTypeAttributeModel.value_is_editable.label('ci_type_attribute_value_is_editable'),
            ConfigItemTypeAttributeModel.value_is_required.label('ci_type_attribute_value_is_required'),
            ConfigItemTypeAttributeModel.value_is_password.label('ci_type_attribute_value_is_password'),
            ConfigItemTypeAttributeModel.value_is_url_link.label('ci_type_attribute_value_is_url_link'),
            ConfigItemTypeAttributeModel.value_re_patterns.label('ci_type_attribute_value_re_patterns'),
            ConfigItemTypeAttributeModel.value_ge_limit_nu.label('ci_type_attribute_value_ge_limit_nu'),
            ConfigItemTypeAttributeModel.value_le_limit_nu.label('ci_type_attribute_value_le_limit_nu')
        )
