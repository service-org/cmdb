#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t
import sqlalchemy as sa

from logging import getLogger
from pydantic import BaseModel
from pydantic import create_model
from collections import namedtuple
from project.service import Service
from pydantic.fields import FieldInfo
from sqlalchemy.orm.query import Query
from project.models.v1.config_item import ConfigItemModel
from service_sqlalchemy.core.client import SQLAlchemyClient
from project.exception.config_item import NotFoundConfigItemError
from project.models.v1.config_item_type import ConfigItemTypeModel
from project.models.v1.config_item_vlaue import ci_value_model_mapping
from project.schema.v1.config_item_vlaue import ci_value_create_schema_mapping
from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeModel
from project.models.v1.config_item_type_attribute_group import ConfigItemTypeAttributeGroupModel

if t.TYPE_CHECKING: from pydantic.main import Model

logger = getLogger(__name__)
CIAttr = namedtuple('CIAttribute', ['id', 'type', 'required'])


class ConfigItemManager(object):
    """ 配置项管理器 """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ 初始化实例

        @param service: 服务对象
        @param session: 会话对象
        """
        self.service = service
        self.session = session

    @staticmethod
    def create_config_item_schema(ci_type_attributes: t.Dict[t.Text, CIAttr]) -> t.Type['Model']:
        """ 根据配置项类型属性构造验证器

        @param ci_type_attributes: 配置项类型属性字典
        @return: BaseModel
        """
        field_definitions = {}
        for code in ci_type_attributes:
            attr = ci_type_attributes[code]
            value_schema = ci_value_create_schema_mapping[attr.type.value]
            value_field_type = value_schema.__fields__['value'].type_
            value_field_info = value_schema.__fields__['value'].field_info
            field_definition = [value_field_type if attr.required else t.Optional[value_field_type], FieldInfo(
                default=value_field_info.default,
                default_factory=value_field_info.default_factory,
                alias=code,
                alias_priority=value_field_info.alias_priority,
                title=value_field_info.title,
                description=value_field_info.description,
                const=value_field_info.const,
                gt=value_field_info.gt,
                ge=value_field_info.ge,
                lt=value_field_info.lt,
                le=value_field_info.le,
                multiple_of=value_field_info.multiple_of,
                min_items=value_field_info.min_items,
                max_items=value_field_info.max_items,
                min_length=value_field_info.min_length,
                max_length=value_field_info.max_length,
                allow_mutation=value_field_info.allow_mutation,
                regex=value_field_info.regex,
                extra=value_field_info.extra
            )]
            field_definitions[code] = tuple(field_definition)
        return create_model('ConfigItemSchema', __base__=BaseModel, **field_definitions)

    def create(self, validated_data: t.Dict[t.Text, t.Any]) -> ConfigItemModel:
        """ 创建配置项

        @param validated_data: 验证后的数据
        @return: ConfigItemModel
        """
        from project.common.manager.config_item_type import ConfigItemTypeManager

        ci_type_id = validated_data.get('ci_type_id', 0)
        query_columns = [ConfigItemTypeAttributeModel.id,
                         ConfigItemTypeAttributeModel.code,
                         ConfigItemTypeAttributeModel.value_type,
                         ConfigItemTypeAttributeModel.value_is_required
                         ]
        ci_type_manager = ConfigItemTypeManager(
            self.service, session=self.session
        )
        ci_type_attributes = ci_type_manager.get_all_ci_type_attributes_by_id(
            ci_type_id, query_columns=query_columns
        )
        ci_type_attributes = {
            o.code: CIAttr(id=o.id, type=o.value_type, required=o.value_is_required) for o in ci_type_attributes
        }
        ConfigItemSchema = self.create_config_item_schema(ci_type_attributes)
        validated_data = ConfigItemSchema.parse_obj(validated_data.get('ci', {})).dict(exclude_unset=True)
        instance = ConfigItemModel(ci_type_id=ci_type_id)
        self.session.add(instance)
        self.session.commit()
        for code, value in validated_data.items():
            attr = ci_type_attributes[code]
            value_type = attr.type.value
            value_model = ci_value_model_mapping[value_type]
            value_inst = value_model(ci_id=instance.id, ci_type_attribute_id=attr.id, value=value)
            self.session.add(value_inst)
        self.session.commit()

        return instance

    def batch_get_by_id(
            self,
            ci_id_list: t.List[int],
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项id列表批量获取配置项

        @param ci_id_list: 配置项id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        query_columns = [ConfigItemModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemModel.id.in_(ci_id_list)]
        queryset = self.session.query(*query_columns).filter(*filter_conditions)
        if queryset.first() or not raise_error: return queryset
        raise NotFoundConfigItemError(f'未找到配置项{ci_id_list}')

    def get_by_id(
            self,
            ci_id: int,
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> Query:
        """ 根据配置项id获取配置项

        @param ci_id: 配置项id
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemModel]
        @param raise_error: 不存在是否抛出异常?
            1. 默认值为False
        @return: Query
        """
        return self.batch_get_by_id([ci_id], query_columns=query_columns, raise_error=raise_error)

    def batch_get_by_ci_type_id(self, ci_type_id_list: t.List[int], query_columns: t.Optional[t.List] = None) -> Query:
        """ 根据配置项类型id列表批量获取配置项

        @param ci_type_id_list: 配置项类型id列表
        @param query_columns: 查询列对象列表
            1. 默认值为[ConfigItemModel]
        @return: Query
        """
        query_columns = [ConfigItemModel] if query_columns is None else query_columns
        filter_conditions = [ConfigItemModel.ci_type_id.in_(ci_type_id_list)]
        return self.session.query(*query_columns).filter(*filter_conditions)

    def get_by_ci_type_id(self, ci_type_id: int, query_columns: t.Optional[t.List] = None) -> Query:
        """ 根据配置项类型id获取配置项

        @param ci_type_id: 配置项类型id
            1. 默认值为[ConfigItemModel]
        @param query_columns: 查询列对象列表
        @return: Query
        """
        return self.batch_get_by_ci_type_id([ci_type_id], query_columns=query_columns)

    def batch_get_ci_value_types_by_id(self, ci_id_list: t.List[int]) -> t.List[t.Text]:
        """ 根据配置项id列表批量获取配置项值类型列表

        @param ci_id_list: 配置项id列表
        @return: t.List[t.Text]
        """
        queryset = self.session.query(
            sa.distinct(ConfigItemTypeAttributeModel.value_type).label('value_type')
        ).join(
            ConfigItemTypeAttributeGroupModel,
            ConfigItemTypeAttributeGroupModel.id == ConfigItemTypeAttributeModel.ci_type_attribute_group_id
        ).join(
            ConfigItemTypeModel,
            ConfigItemTypeModel.id == ConfigItemTypeAttributeGroupModel.ci_type_id
        ).join(
            ConfigItemModel,
            ConfigItemModel.ci_type_id == ConfigItemTypeModel.id
        ).filter(
            ConfigItemModel.id.in_(ci_id_list)
        )
        return [ins.value_type.value for ins in queryset]

    def get_ci_value_types_by_id(self, ci_id: int) -> t.List[t.Text]:
        """ 根据配置项id获取配置项值类型列表

        @param ci_id: 配置项id
        @return: t.List[t.Text]
        """
        return self.batch_get_ci_value_types_by_id([ci_id])

    def batch_update_by_id(self, ci_id_list: t.List[int], validated_data: t.List[t.Dict[t.Text, t.Any]]) -> None:
        """ 根据配置项id列表批量更新配置项

        @param ci_id_list: 配置项id列表
        @param validated_data: 验证后的数据
        @return: None
        """
        from project.common.manager.config_item_vlaue import ConfigItemVlaueProxyManager

        ci_value_manager = ConfigItemVlaueProxyManager(
            self.service, session=self.session
        )
        ci_value_manager.batch_update_by_ci_id_and_ci_type_attribute_id(
            ci_id_list, validated_data=validated_data
        )

    def update_by_id(self, ci_id: int, validated_data: t.Dict[t.Text, t.Any]) -> None:
        """ 根据配置项id更新配置项

        @param ci_id: 配置项id
        @param validated_data: 验证后的数据
        @return: None
        """
        from project.common.manager.config_item_vlaue import ConfigItemVlaueProxyManager

        ci_value_manager = ConfigItemVlaueProxyManager(
            self.service, session=self.session
        )
        ci_value_manager.update_by_ci_id_and_ci_type_attribute_id(
            ci_id, validated_data=validated_data
        )

    def batch_delete_by_id(self, ci_id_list: t.List[id]) -> None:
        """ 根据配置项id列表批量删除配置项

        @param ci_id_list: 配置项id列表
        @return: None
        """
        from project.common.manager.config_item_vlaue import ConfigItemVlaueProxyManager

        queryset = self.batch_get_by_id(ci_id_list, raise_error=False)
        ci_value_manager = ConfigItemVlaueProxyManager(
            self.service, session=self.session
        )
        ci_value_manager.batch_delete_by_ci_id(ci_id_list)
        queryset.delete(synchronize_session=False)

    def delete_by_id(self, ci_id: id) -> None:
        """ 根据配置项id删除配置项

        @param ci_id: 配置项id
        @return: None
        """
        from project.common.manager.config_item_vlaue import ConfigItemVlaueProxyManager

        queryset = self.get_by_id(ci_id, raise_error=True)
        ci_value_manager = ConfigItemVlaueProxyManager(
            self.service, session=self.session
        )
        ci_value_manager.delete_by_ci_id(ci_id)
        queryset.delete(synchronize_session=False)
