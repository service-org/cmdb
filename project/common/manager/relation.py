#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from project.service import Service
from sqlalchemy.orm.query import Query
from project.models.v1.relation import RelationModel
from service_sqlalchemy.core.client import SQLAlchemyClient
from project.exception.relation import NotFoundRelationError
from project.exception.relation.create import DuplicatedRelationError
from project.exception.relation.delete import NotAllowedDeleteRelationThatHasReferencedError

logger = getLogger(__name__)


class RelationManager(object):
    """ 关联关系管理器 """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ 初始化实例

        @param service: 服务对象
        @param session: 会话对象
        """
        self.service = service
        self.session = session

    def check_create_duplication(self, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 检查创建时是否存在重复关联关系

        @param validated_data: 验证后的数据
        @return: None
        """
        code = validated_data.get('code', '')
        name = validated_data.get('name', '')
        query_columns = [RelationModel.id]
        filter_conditions = [RelationModel.code == code]
        if not self.session.query(*query_columns).filter(*filter_conditions).first(): return
        raise DuplicatedRelationError(f'数据唯一性校验失败，{name}({code}) 重复')

    def create(self, validated_data: t.Dict[t.Text, t.Any]) -> RelationModel:
        """ 创建指定关联关系

        @param validated_data: 验证后的数据
        @return: ConfigItemTypeGroupModel
        """
        self.check_create_duplication(
            validated_data
        )
        instance = RelationModel(
            **validated_data
        )
        self.session.add(instance)
        self.session.commit()

        return instance

    def batch_get_by_id(
            self,
            relation_id_list: t.List[int],
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据关联关系id列表批量获取关联关系

        @param relation_id_list: 关联关系id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[RelationModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        query_columns = [RelationModel] if query_columns is None else query_columns
        filter_conditions = [RelationModel.id.in_(relation_id_list)]
        queryset = self.session.query(*query_columns).filter(*filter_conditions)
        if queryset.first() or not raise_error: return queryset
        raise NotFoundRelationError(f'未找到关联关系{relation_id_list}')

    def get_by_id(
            self,
            relation_id: int,
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据关联关系id获取关联关系

        @param relation_id: 关联关系id
        @param query_columns: 查询列对象列表
            1. 默认值为[RelationModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        return self.batch_get_by_id([relation_id], query_columns=query_columns, raise_error=raise_error)

    def batch_update_by_id(self, relation_id_list: t.List[int], validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据关联关系id列表批量更新关联关系

        @param relation_id_list: 关联关系id列表
        @param validated_data: 验证后的数据
        @return: None
        """
        queryset = self.batch_get_by_id(relation_id_list, raise_error=False)
        queryset.update(validated_data)

    def update_by_id(self, relation_id: int, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据关联关系id更新关联关系

        @param relation_id: 关联关系id
        @param validated_data: 验证后的数据
        @return: None
        """
        instance = self.get_by_id(
            relation_id, raise_error=True
        ).first()
        for k, v in validated_data.items():
            setattr(instance, k, v)

    def batch_delete_by_id(self, relation_id_list: t.List[int]) -> None:
        """ 根据关联关系id列表批量删除关联关系

        @param relation_id_list: 关联关系id列表
        @return: None
        """
        queryset = self.batch_get_by_id(relation_id_list, raise_error=False)
        queryset.delete(synchronize_session=False)

    def delete_by_id(self, relation_id: int) -> None:
        """ 根据关联关系id删除关联关系

        @param relation_id: 关联关系id
        @return: None
        """
        queryset = self.get_by_id(relation_id, raise_error=True)
        instance = queryset.first()
        ci_cis = instance.ci_relation_ci_cis
        ci_type_ci_types = instance.ci_type_relation_ci_type_ci_types
        if not ci_cis and not ci_type_ci_types: return queryset.delete(synchronize_session=False)
        raise NotAllowedDeleteRelationThatHasReferencedError('关联类型已经被引用,不允许删除')

    def get_all(self, query_columns: t.Optional[t.List] = None) -> Query:
        """ 获取所有关联关系

        @param query_columns: 查询列对象列表
        @return: Query
        """
        query_columns = [RelationModel] if query_columns is None else query_columns
        return self.session.query(*query_columns)
