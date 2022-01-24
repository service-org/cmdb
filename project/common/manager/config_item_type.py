#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t
import sqlalchemy as sa

from project.service import Service
from sqlalchemy.orm.query import Query
from project.models.v1.config_item import ConfigItemModel
from service_sqlalchemy.core.client import SQLAlchemyClient
from project.models.v1.config_item_type import ConfigItemTypeModel
from project.exception.config_item_type import NotFoundConfigItemTypeError
from project.models.v1.config_item_type_group import ConfigItemTypeGroupModel
from project.exception.config_item_type.create import DuplicatedConfigItemTypeError
from project.common.manager.config_item_type_group import ConfigItemTypeGroupManager
from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeModel
from project.common.manager.config_item_type_attribute import ConfigItemTypeAttributeManager
from project.models.v1.config_item_type_attribute_group import ConfigItemTypeAttributeGroupModel
from project.models.v1.config_item_type_config_item_types import ConfigItemTypeConfigItemTypesModel
from project.common.manager.config_item_type_attribute_group import ConfigItemTypeAttributeGroupManager
from project.exception.config_item_type.delete import NotAllowedDeleteConfigItemTypeThatHasReferencedError
from project.exception.config_item_type.delete import NotAllowedDeleteConfigItemTypeThatHasInstantiatedError


class ConfigItemTypeManager(object):
    """ 配置项类型管理器 """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ 初始化实例

        @param service: 服务对象
        @param session: 会话对象
        """
        self.service = service
        self.session = session

    def check_create_duplication(self, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 检查创建时是否存在重复配置项类型

        @param validated_data: 验证后的数据
        @return: None
        """
        code = validated_data.get('code', '')
        name = validated_data.get('name', '')
        query_columns = [ConfigItemTypeModel.id]
        filter_conditions = [ConfigItemTypeModel.code == code]
        if not self.session.query(*query_columns).filter(*filter_conditions).first(): return
        raise DuplicatedConfigItemTypeError(f'数据唯一性校验失败，{name}({code}) 重复')

    def create(self, validated_data: t.Dict[t.Text, t.Any]) -> ConfigItemTypeModel:
        """ 创建配置项类型

        @param validated_data: 验证后的数据
        @return: ConfigItemTypeModel
        """
        ci_type_group_id = validated_data.get('ci_type_group_id', 0)
        self.check_create_duplication(
            validated_data
        )
        ci_type_group_manager = ConfigItemTypeGroupManager(
            self.service, session=self.session
        )
        ci_type_group_manager.get_by_id(
            ci_type_group_id,
            query_columns=[ConfigItemTypeGroupModel.id],
            raise_error=True
        )
        instance = ConfigItemTypeModel(
            **validated_data
        )
        self.session.add(instance)
        self.session.commit()

        return instance

    def batch_get_by_id(
            self,
            ci_type_id_list: t.List[int],
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项类型id列表获取配置项类型

        @param ci_type_id_list: 配置项类型id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        query_columns = [ConfigItemTypeModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemTypeModel.id.in_(ci_type_id_list)]
        queryset = self.session.query(*query_columns).filter(*filter_conditions)
        if queryset.first() or not raise_error: return queryset
        raise NotFoundConfigItemTypeError(f'未找到配置项类型{ci_type_id_list}')

    def get_by_id(
            self,
            ci_type_id: int,
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项类型id获取配置项类型

        @param ci_type_id: 配置项类型id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: t.Union[Query, None]
        """
        return self.batch_get_by_id([ci_type_id], query_columns=query_columns, raise_error=raise_error)

    def batch_get_by_ci_type_group_id(
            self,
            ci_type_group_id_list: t.List[int],
            query_columns: t.Optional[t.List] = None
    ) -> Query:
        """ 根据配置项类型分组id列表批量获取配置项类型

        @param ci_type_group_id_list: 配置项类型分组id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeModel]
        @return: Query
        """
        query_columns = [ConfigItemTypeModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemTypeModel.ci_type_group_id.in_(ci_type_group_id_list)]
        return self.session.query(*query_columns).filter(*filter_conditions)

    def get_by_ci_type_group_id(
            self,
            ci_type_group_id: int,
            query_columns: t.Optional[t.List] = None
    ) -> Query:
        """ 根据配置项类型分组id获取配置项类型

        @param ci_type_group_id: 配置项类型分组id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemTypeModel]
        @return: Query
        """
        return self.batch_get_by_ci_type_group_id([ci_type_group_id], query_columns=query_columns)

    def batch_update_by_id(self, ci_type_id_list: t.List[int], validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置项类型id列表批量更新配置项类型

        @param ci_type_id_list: 配置项类型id列表
        @param validated_data: 验证后的数据
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_id_list, raise_error=False)
        queryset.update(validated_data)

    def update_by_id(self, ci_type_id: int, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置项类型id更新配置项类型

        @param ci_type_id: 配置项类型id
        @param validated_data: 验证后的数据
        @return: None
        """
        instance = self.get_by_id(
            ci_type_id, raise_error=True
        ).first()
        for k, v in validated_data.items():
            setattr(instance, k, v)

    def batch_delete_by_id(self, ci_type_id_list: t.List[int]) -> None:
        """ 根据配置项类型id列表批量删除配置项类型

        @param ci_type_id_list: 配置类型id列表
        @return: None
        """
        queryset = self.batch_get_by_id(ci_type_id_list, raise_error=False)
        queryset.delete(synchronize_session=False)

    def delete_by_id(self, ci_type_id: int) -> None:
        """ 根据配置项类型id删除配置项类型

        @param ci_type_id: 配置项类型id
        @return: None
        """
        from project.common.manager.config_item import ConfigItemManager

        queryset = self.get_by_id(
            ci_type_id, query_columns=[ConfigItemTypeModel.id], raise_error=True
        )
        instance = queryset.first()
        ci_manager = ConfigItemManager(
            self.service, session=self.session
        )
        if ci_manager.get_by_ci_type_id(
                ci_type_id, query_columns=[ConfigItemModel.id]
        ).first():
            raise NotAllowedDeleteConfigItemTypeThatHasInstantiatedError('配置项类型存在实例引用,不允许删除')
        if self.session.query(
            ConfigItemTypeConfigItemTypesModel.id
        ).filter(
            sa.or_(ConfigItemTypeConfigItemTypesModel.ci_type_source_id == instance.id,
                   ConfigItemTypeConfigItemTypesModel.ci_type_target_id == instance.id)
        ).first():
            raise NotAllowedDeleteConfigItemTypeThatHasReferencedError('配置项类型被关联引用,不允许删除')
        ci_type_attribute_group_manager = ConfigItemTypeAttributeGroupManager(
            self.service, session=self.session
        )
        ci_type_attribute_groups = ci_type_attribute_group_manager.get_by_ci_type_id(
            ci_type_id, query_columns=[ConfigItemTypeAttributeGroupModel.id]
        )
        ci_type_attribute_group_id_list = [ins.id for ins in ci_type_attribute_groups]
        ci_type_attribute_manager = ConfigItemTypeAttributeManager(
            self.service, session=self.session
        )
        ci_type_attribute_manager.batch_delete_by_ci_type_attribute_group_id(
            ci_type_attribute_group_id_list
        )
        ci_type_attribute_group_manager.get_by_ci_type_id(ci_type_id).delete(synchronize_session=False)
        self.get_by_id(ci_type_id).delete(synchronize_session=False)

    def get_all_ci_type_attributes_by_id(self, ci_type_id: int, query_columns: t.Optional[t.List] = None) -> Query:
        """ 根据配置项类型id获取所有配置项类型属性

        @param ci_type_id: 配置项类型id
        @param query_columns: 查询列对象列表
        @return: Query
        """
        query_columns = [ConfigItemTypeAttributeModel] if query_columns is None else query_columns
        return self.session.query(
            *query_columns
        ).join(
            ConfigItemTypeAttributeGroupModel,
            ConfigItemTypeAttributeGroupModel.id == ConfigItemTypeAttributeModel.ci_type_attribute_group_id
        ).join(
            ConfigItemTypeModel,
            ConfigItemTypeModel.id == ConfigItemTypeAttributeGroupModel.ci_type_id
        ).filter(
            ConfigItemTypeModel.id == ci_type_id
        )
