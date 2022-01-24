#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from project.service import Service
from sqlalchemy.orm.query import Query
from service_sqlalchemy.core.client import SQLAlchemyClient
from project.models.v1.config_item_type import ConfigItemTypeModel
from project.models.v1.config_item_type_group import ConfigItemTypeGroupModel
from project.exception.config_item_type_group import NotFoundConfigItemTypeGroupError
from project.exception.config_item_type_group.create import DuplicatedConfigItemTypeGroupError
from project.exception.config_item_type_group.delete import NotAllowedDeleteGroupThatHasConfigItemTypeError

logger = getLogger(__name__)


class ConfigItemTypeGroupManager(object):
    """ 配置项类型分组管理器 """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ 初始化实例

        @param service: 服务对象
        @param session: 会话对象
        """
        self.service = service
        self.session = session

    def check_create_duplication(self, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 检查创建时是否存在重复配置项类型分组

        @param validated_data: 验证后的数据
        @return: None
        """
        code = validated_data.get('code', '')
        name = validated_data.get('name', '')
        query_columns = [ConfigItemTypeGroupModel.id]
        filter_conditions = [ConfigItemTypeGroupModel.code == code]
        if not self.session.query(*query_columns).filter(*filter_conditions).first(): return
        raise DuplicatedConfigItemTypeGroupError(f'数据唯一性校验失败，{name}({code}) 重复')

    def create(self, validated_data: t.Dict[t.Text, t.Any]) -> ConfigItemTypeGroupModel:
        """ 创建指定配置项类型分组

        @param validated_data: 验证后的数据
        @return: ConfigItemTypeGroupModel
        """
        self.check_create_duplication(
            validated_data
        )
        instance = ConfigItemTypeGroupModel(
            **validated_data
        )
        self.session.add(instance)
        self.session.commit()

        return instance

    def batch_get_by_id(
            self,
            ci_type_group_id_list: t.List[int],
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项类型分组id列表获取配置项类型分组

        @param ci_type_group_id_list: 配置项类型分组id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeGroupModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        query_columns = [ConfigItemTypeGroupModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemTypeGroupModel.id.in_(ci_type_group_id_list)]
        queryset = self.session.query(*query_columns).filter(*filter_conditions)
        if queryset.first() or not raise_error: return queryset
        raise NotFoundConfigItemTypeGroupError(f'未找到配置项类型分组{ci_type_group_id_list}')

    def get_by_id(
            self,
            ci_type_group_id: int,
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项类型分组id获取配置项类型分组

        @param ci_type_group_id: 配置项类型分组id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeGroupModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: t.Union[Query, None]
        """
        return self.batch_get_by_id([ci_type_group_id], query_columns=query_columns, raise_error=raise_error)

    def batch_update_by_id(self, ci_type_group_id_list: t.List[int], validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置项类型分组id列表批量更新配置项类型分组

        @param ci_type_group_id_list: 配置项类型分组id列表
        @param validated_data: 验证后的数据
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_group_id_list, raise_error=False)
        queryset.update(validated_data)

    def update_by_id(self, ci_type_group_id: int, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置项类型分组id更新配置项类型分组

        @param ci_type_group_id: 配置项类型分组id
        @param validated_data: 验证后的数据
        @return: None
        """
        instance = self.get_by_id(
            ci_type_group_id, raise_error=True
        ).first()
        for k, v in validated_data.items():
            setattr(instance, k, v)

    def batch_delete_by_id(self, ci_type_group_id_list: t.List[int]) -> None:
        """ 根据配置项类型分组id列表批量删除配置项类型分组

        @param ci_type_group_id_list: 配置项类型分组id列表
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_group_id_list, raise_error=False)
        queryset.delete(synchronize_session=False)

    def delete_by_id(self, ci_type_group_id: int) -> None:
        """ 根据配置项类型分组id删除配置项类型分组

        @param ci_type_group_id: 配置项类型分组id
        @return: None
        """
        queryset = self.get_by_id(ci_type_group_id, raise_error=True)
        instance = queryset.first()
        ci_types = instance.ci_type_group_ci_types
        if not ci_types: return queryset.delete(synchronize_session=False)
        raise NotAllowedDeleteGroupThatHasConfigItemTypeError('分组下有配置项类型,不允许删除')

    def get_all(self, query_columns: t.Optional[t.List] = None) -> Query:
        """ 获取所有配置项类型分组

        @param query_columns: 查询列对象列表
        @return: Query
        """
        query_columns = [ConfigItemTypeGroupModel] if query_columns is None else query_columns
        return self.session.query(*query_columns)

    def get_all_ci_types(self) -> Query:
        """ 获取所有配置项类型分组下配置项类型

        @return: Query
        """
        return self.session.query(
            ConfigItemTypeGroupModel.id,
            ConfigItemTypeGroupModel.code,
            ConfigItemTypeGroupModel.name,
            ConfigItemTypeGroupModel.order,
            ConfigItemTypeGroupModel.is_built_in,
            ConfigItemTypeModel.id.label('ci_type_id'),
            ConfigItemTypeModel.code.label('ci_type_code'),
            ConfigItemTypeModel.name.label('ci_type_name'),
            ConfigItemTypeModel.icon.label('ci_type_icon'),
            ConfigItemTypeModel.desc.label('ci_type_desc'),
            ConfigItemTypeModel.order.label('ci_type_order'),
            ConfigItemTypeModel.is_built_in.label('ci_type_is_built_in'),
            ConfigItemTypeModel.is_disabled.label('ci_type_is_disabled'),
            ConfigItemTypeModel.is_not_show.label('ci_type_is_not_show')
        ).join(
            ConfigItemTypeGroupModel,
            ConfigItemTypeGroupModel.id == ConfigItemTypeModel.ci_type_group_id
        )
