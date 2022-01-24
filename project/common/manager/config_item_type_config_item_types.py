#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from project.service import Service
from sqlalchemy.orm.query import Query
from service_sqlalchemy.core.client import SQLAlchemyClient
from project.models.v1.config_item_type_config_item_types import ConfigItemTypeConfigItemTypesModel
from project.exception.config_item_type_config_item_types import NotFoundConfigItemTypeConfigItemTypesError
from project.exception.config_item_type_config_item_types.create import DuplicatedConfigItemTypeConfigItemTypesError

logger = getLogger(__name__)


class ConfigItemTypeConfigItemTypesManager(object):
    """ 配置项类型与配置项类型关联关系管理器 """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ 初始化实例

        @param service: 服务对象
        @param session: 会话对象
        """
        self.service = service
        self.session = session

    def check_create_duplication(self, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 检查创建时是否存在重复配置项类型与配置项类型关联关系

        @param validated_data: 验证后的数据
        @return: None
        """
        ci_type_source_id = validated_data.get('ci_type_source_id', 0)
        ci_type_relation_id = validated_data.get('ci_type_relation_id', 0)
        ci_type_target_id = validated_data.get('ci_type_target_id', 0)
        query_columns = [ConfigItemTypeConfigItemTypesModel.id]
        filter_conditions = [ConfigItemTypeConfigItemTypesModel.ci_type_source_id == ci_type_source_id,
                             ConfigItemTypeConfigItemTypesModel.ci_type_relation_id == ci_type_relation_id,
                             ConfigItemTypeConfigItemTypesModel.ci_type_target_id == ci_type_target_id]
        if not self.session.query(*query_columns).filter(*filter_conditions).first(): return
        err_mesg = f'来源ID({ci_type_source_id})-关系ID({ci_type_relation_id})-目标ID({ci_type_target_id})'
        raise DuplicatedConfigItemTypeConfigItemTypesError(f'数据唯一性校验失败，{err_mesg} 重复')

    def create(self, validated_data: t.Dict[t.Text, t.Any]) -> ConfigItemTypeConfigItemTypesModel:
        """ 创建指定配置项类型与配置项类型关联关系

        @param validated_data: 验证后的数据
        @return: ConfigItemTypeConfigItemTypesModel
        """
        self.check_create_duplication(
            validated_data
        )
        instance = ConfigItemTypeConfigItemTypesModel(
            **validated_data
        )
        self.session.add(instance)
        self.session.commit()

        return instance

    def batch_get_by_id(
            self,
            ci_type_ci_types_id_list: t.List[int],
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项类型与配置项类型关联关系id列表获取配置项类型与配置项类型关联关系

        @param ci_type_ci_types_id_list: 配置项类型与配置项类型关联关系id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeConfigItemTypesModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        query_columns = [ConfigItemTypeConfigItemTypesModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemTypeConfigItemTypesModel.id.in_(ci_type_ci_types_id_list)]
        queryset = self.session.query(*query_columns).filter(*filter_conditions)
        if queryset.first.first() or not raise_error: return queryset
        raise NotFoundConfigItemTypeConfigItemTypesError(f'未找到配置项类型与配置项类型关联关系{ci_type_ci_types_id_list}')

    def get_by_id(
            self,
            ci_type_ci_types_id: int,
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项类型与配置项类型关联关系id获取配置项类型与配置项类型关联关系

        @param ci_type_ci_types_id: 配置项类型与配置项类型关联关系id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeConfigItemTypesModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        return self.batch_get_by_id([ci_type_ci_types_id], query_columns=query_columns, raise_error=raise_error)

    def batch_update_by_id(self, ci_type_ci_types_id_list: t.List[int], validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置项类型与配置项类型关联关系id列表批量更新配置项类型与配置项类型关联关系

        @param ci_type_ci_types_id_list: 配置项类型与配置项类型关联关系id列表
        @param validated_data: 验证后的数据
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_ci_types_id_list, raise_error=False)
        queryset.update(validated_data)

    def update_by_id(self, ci_type_ci_types_id: int, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置项类型与配置项类型关联关系id更新配置项类型与配置项类型关联关系

        @param ci_type_ci_types_id: 配置项类型与配置项类型关联关系id
        @param validated_data: 验证后的数据
        @return: None
        """
        instance = self.get_by_id(
            ci_type_ci_types_id, raise_error=True
        ).first()
        for k, v in validated_data.items():
            setattr(instance, k, v)

    def batch_delete_by_id(self, ci_type_ci_types_id_list: t.List[int]) -> None:
        """ 根据配置项类型与配置项类型关联关系id列表批量删除配置项类型与配置项类型关联关系

        @param ci_type_ci_types_id_list: 配置项类型与配置项类型关联关系id列表
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_ci_types_id_list, raise_error=False)
        queryset.delete(synchronize_session=False)

    def delete_by_id(self, ci_type_ci_types_id: int) -> None:
        """ 根据配置项类型与配置项类型关联关系id删除配置项类型与配置项类型关联关系

        @param ci_type_ci_types_id: 配置项类型与配置项类型关联关系id
        @return: None
        """
        queryset = self.get_by_id(ci_type_ci_types_id, raise_error=True)
        queryset.delete(synchronize_session=False)

    def get_all(self, query_columns: t.Optional[t.List] = None) -> Query:
        """ 获取所有配置项类型与配置项类型关联关系

        @param query_columns: 查询列对象列表
        @return: Query
        """
        query_columns = [ConfigItemTypeConfigItemTypesModel] if query_columns is None else query_columns
        return self.session.query(*query_columns)
