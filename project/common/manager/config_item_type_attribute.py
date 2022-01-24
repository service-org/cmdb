#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from project.service import Service
from sqlalchemy.orm.query import Query
from service_sqlalchemy.core.client import SQLAlchemyClient
from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeModel
from project.exception.config_item_type_attribute import NotFoundConfigItemTypeAttributeError
from project.models.v1.config_item_type_attribute_group import ConfigItemTypeAttributeGroupModel
from project.common.manager.config_item_type_attribute_group import ConfigItemTypeAttributeGroupManager


class ConfigItemTypeAttributeManager(object):
    """ 配置项类型属性管理器 """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ 初始化实例

        @param service: 服务对象
        @param session: 会话对象
        """
        self.service = service
        self.session = session

    def check_create_duplication(self, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 检查创建时是否存在重复配置项类型属性

        @param validated_data: 验证后的数据
        @return: None
        """
        code = validated_data.get('code', '')
        name = validated_data.get('name', '')
        ci_type_attribute_group_id = validated_data.get('ci_type_attribute_group_id', 0)
        ci_type_attribute_group_manager = ConfigItemTypeAttributeGroupManager(self.service, session=self.session)
        ci_type_id = ci_type_attribute_group_manager.get_by_id(
            ci_type_attribute_group_id,
            query_columns=[ConfigItemTypeAttributeGroupModel.ci_type_id], raise_error=True
        ).scalar()
        if not self.session.query(
            ConfigItemTypeAttributeModel.id
        ).join(
            ConfigItemTypeAttributeGroupModel,
            ConfigItemTypeAttributeGroupModel.id == ConfigItemTypeAttributeModel.ci_type_attribute_group_id
        ).filter(
            ConfigItemTypeAttributeGroupModel.ci_type_id == ci_type_id,
            ConfigItemTypeAttributeModel.code == code
        ).first():
            return
        raise NotFoundConfigItemTypeAttributeError(f'数据唯一性校验失败，{name}({code}) 重复')

    def create(self, validated_data: t.Dict[t.Text, t.Any]) -> ConfigItemTypeAttributeModel:
        """ 创建指定配置项类型属性

        @param validated_data: 验证后的数据
        @return: ConfigItemTypeAttributeGroupModel
        """
        self.check_create_duplication(
            validated_data
        )
        instance = ConfigItemTypeAttributeModel(
            **validated_data
        )
        self.session.add(instance)
        self.session.commit()

        return instance

    def batch_get_by_id(
            self,
            ci_type_attribute_id_list: t.List[int],
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项类型属性id列表获取配置项类型属性

        @param ci_type_attribute_id_list: 配置项类型属性id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeAttributeModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        query_columns = [ConfigItemTypeAttributeModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemTypeAttributeModel.id.in_(ci_type_attribute_id_list)]
        queryset = self.session.query(*query_columns).filter(*filter_conditions)
        if queryset.first() or not raise_error: return queryset
        raise NotFoundConfigItemTypeAttributeError(f'未找到配置项类型属性{ci_type_attribute_id_list}')

    def get_by_id(
            self,
            ci_type_attribute_id: int,
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项类型属性id获取配置项类型属性

        @param ci_type_attribute_id: 配置项类型属性id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeAttributeModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        return self.batch_get_by_id([ci_type_attribute_id], query_columns=query_columns, raise_error=raise_error)

    def batch_update_by_id(self, ci_type_attribute_id_list: t.List[int], validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置项类型属性id列表批量更新配置项类型属性

        @param ci_type_attribute_id_list: 配置项类型属性id列表
        @param validated_data: 验证后的数据
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_attribute_id_list, raise_error=False)
        queryset.update(validated_data)

    def update_by_id(self, ci_type_attribute_id: int, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置类型属性id更新配置类型属性

        @param ci_type_attribute_id: 配置类型属性id
        @param validated_data: 验证后的数据
        @return: None
        """
        instance = self.get_by_id(
            ci_type_attribute_id, raise_error=True
        ).first()
        for k, v in validated_data.items():
            setattr(instance, k, v)

    def batch_delete_by_id(self, ci_type_attribute_id_list: t.List[int]) -> None:
        """ 根据配置项类型属性id列表批量删除配置项类型属性

        @param ci_type_attribute_id_list: 配置项类型属性id
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_attribute_id_list, raise_error=False)
        queryset.delete(synchronize_session=False)

    def delete_by_id(self, ci_type_attribute_id: int) -> None:
        """ 根据配置项类型属性id删除配置项类型属性

        @param ci_type_attribute_id: 配置项类型属性分组id
        @return: None
        """
        queryset = self.get_by_id(ci_type_attribute_id, raise_error=True)
        queryset.delete(synchronize_session=False)

    def batch_get_by_ci_type_attribute_group_id(
            self, ci_type_attribute_group_id_list: t.List[int],
            query_columns: t.Optional[t.List] = None
    ) -> Query:
        """ 根据配置项类型属性分组id列表批量获取配置项类型属性

        @param ci_type_attribute_group_id_list: 配置项类型属性分组id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeAttributeModel]
        @return: Query
        """
        query_columns = [ConfigItemTypeAttributeModel] if query_columns is None else query_columns
        filter_conditions = [
            ConfigItemTypeAttributeModel.ci_type_attribute_group_id.in_(ci_type_attribute_group_id_list)
        ]
        return self.session.query(*query_columns).filter(*filter_conditions)

    def get_by_ci_type_attribute_group_id(
            self,
            ci_type_attribute_group_id: int,
            query_columns: t.Optional[t.List] = None
    ) -> Query:
        """ 根据配置项类型属性分组id获取配置项类型属性

        @param ci_type_attribute_group_id: 配置项类型属性分组id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeAttributeModel]
        @return: Query
        """
        return self.batch_get_by_ci_type_attribute_group_id([ci_type_attribute_group_id], query_columns=query_columns)

    def batch_delete_by_ci_type_attribute_group_id(self, ci_type_attribute_group_id_list: t.List[int]) -> None:
        """ 根据配置项类型属性分组id列表批量删除配置项类型属性

        @param ci_type_attribute_group_id_list: 配置项类型属性id
        @return: None
        """
        queryset = self.batch_get_by_ci_type_attribute_group_id(ci_type_attribute_group_id_list)
        queryset.delete(synchronize_session=False)

    def delete_by_ci_type_attribute_group_id(self, ci_type_attribute_group_id: int) -> None:
        """ 根据配置项类型属性分组id删除配置项类型属性

        @param ci_type_attribute_group_id: 配置项类型属性分组id
        @return: None
        """
        self.batch_delete_by_ci_type_attribute_group_id([ci_type_attribute_group_id])
