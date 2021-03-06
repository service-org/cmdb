#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from project.service import Service
from sqlalchemy.orm.query import Query
from project.models.v1.config_item import ConfigItemModel
from service_sqlalchemy.core.client import SQLAlchemyClient
from project.models.v1.config_item_vlaue import ci_value_model_mapping
from project.exception.config_item_vlaue import NotFoundConfigItemValueError
from project.schema.v1.config_item_vlaue import ci_value_update_schema_mapping
from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeModel
from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeValueType
from project.common.manager.config_item_type_attribute import ConfigItemTypeAttributeManager

from .config_item_bool_value import ConfigItemBoolValueManager
from .config_item_date_value import ConfigItemDateValueManager
from .config_item_datetime_value import ConfigItemDatetimeValueManager
from .config_item_float_value import ConfigItemFloatValueManager
from .config_item_int_value import ConfigItemIntValueManager
from .config_item_json_value import ConfigItemJsonValueManager
from .config_item_text_value import ConfigItemTextValueManager
from .config_item_textarea_value import ConfigItemTextareaValueManager
from .config_item_time_value import ConfigItemTimeValueManager
from .config_item_timezone_value import ConfigItemTimezoneValueManager
from .config_item_user_value import ConfigItemUserValueManager

ci_value_manager_mapping = {
    ConfigItemTypeAttributeValueType.BOOL.value: ConfigItemBoolValueManager,
    ConfigItemTypeAttributeValueType.DATE.value: ConfigItemDateValueManager,
    ConfigItemTypeAttributeValueType.DATETIME.value: ConfigItemDatetimeValueManager,
    ConfigItemTypeAttributeValueType.FLOAT.value: ConfigItemFloatValueManager,
    ConfigItemTypeAttributeValueType.INT.value: ConfigItemIntValueManager,
    ConfigItemTypeAttributeValueType.JSON.value: ConfigItemJsonValueManager,
    ConfigItemTypeAttributeValueType.TEXT.value: ConfigItemTextValueManager,
    ConfigItemTypeAttributeValueType.TEXTAREA.value: ConfigItemTextareaValueManager,
    ConfigItemTypeAttributeValueType.TIME.value: ConfigItemTimeValueManager,
    ConfigItemTypeAttributeValueType.TIMEZONE.value: ConfigItemTimezoneValueManager,
    ConfigItemTypeAttributeValueType.USER.value: ConfigItemUserValueManager
}

class ConfigItemVlaueProxyManager(object):
    """ ??????????????????????????? """

    def __init__(self, service: Service, session: SQLAlchemyClient) -> None:
        """ ???????????????

        @param service: ????????????
        @param session: ????????????
        """
        self.service = service
        self.session = session

    def batch_get_by_ci_id(
            self,
            ci_id_list: t.List[int],
            value_type: t.Text,
            query_columns: t.Optional[t.List] = None
    ) -> Query:
        """ ???????????????id??????????????????????????????

        @param ci_id_list: ?????????id??????
        @param value_type: ??????????????????
        @param query_columns: ?????????????????????
        @param query_columns: ?????????????????????
            1. ????????????ci_value_model_mapping[value_type]
        @return: Query
        """
        value_model = ci_value_model_mapping[value_type]
        query_columns = [value_model] if query_columns is None else query_columns
        filter_conditions = [value_model.ci_id.in_(ci_id_list)]
        return self.session.query(*query_columns).filter(*filter_conditions)

    def get_by_ci_id(
            self,
            ci_id: int,
            value_type: t.Text,
            query_columns: t.Optional[t.List] = None
    ) -> Query:
        """ ???????????????id??????????????????????????????

        @param ci_id: ?????????id
        @param value_type: ??????????????????
        @param query_columns: ?????????????????????
            1. ????????????ci_value_model_mapping[value_type]
        @return: Query
        """
        value_model = ci_value_model_mapping[value_type]
        query_columns = [value_model] if query_columns is None else query_columns
        return self.batch_get_by_ci_id([ci_id], value_type=value_type, query_columns=query_columns)

    def get_by_ci_id_and_ci_type_attribute_id(
            self,
            ci_id: int,
            ci_type_attribute_id: int,
            value_type: t.Text,
            query_columns: t.Optional[t.List] = None,
            raise_error: t.Optional[bool] = False
    ) -> ConfigItemModel:
        """ ???????????????id????????????????????????id??????????????????

        @param ci_id: ?????????id
        @param ci_type_attribute_id: ?????????????????????id
        @param value_type: ???????????????
        @param query_columns: ?????????????????????
            1. ????????????ci_value_model_mapping[value_type]
        @param raise_error: ???????????????????
            1. ????????????False
        @return: ConfigItemModel
        """

        value_model = ci_value_model_mapping[value_type]
        query_columns = [value_model] if query_columns is None else query_columns
        filter_conditions = [value_model.ci_id == ci_id, value_model.ci_type_attribute_id == ci_type_attribute_id]
        queryset = self.session.query(*query_columns).filter(*filter_conditions)
        if queryset.first() or not raise_error: return queryset
        raise NotFoundConfigItemValueError('?????????????????????{}'.format({'ci_id': ci_id, 'ci_type_attribute_id': ci_type_attribute_id}))

    def batch_update_by_ci_id_and_ci_type_attribute_id(
            self,
            ci_id_list: t.List[int],
            validated_data: t.List[t.Dict[t.Text, t.Any]]
    ) -> None:
        """ ???????????????id??????????????????????????????id???????????????????????????????????????

        @param ci_id_list: ?????????id??????
        @param validated_data: ??????????????????
        @return: None
        """
        for ci_id in ci_id_list:
            for data in validated_data: self.update_by_ci_id_and_ci_type_attribute_id(ci_id, validated_data=data)

    def update_by_ci_id_and_ci_type_attribute_id(
            self,
            ci_id: int,
            validated_data: t.Dict[t.Text, t.Any]
    ) -> None:
        """ ???????????????id????????????????????????id???????????????????????????

        @param ci_id: ?????????id
        @param validated_data: ?????????????????????id
        @return: None
        """
        ci_type_attribute_manager = ConfigItemTypeAttributeManager(
            self.service, session=self.session
        )
        ci_type_attribute_id = validated_data.get('ci_type_attribute_id', 0)
        value = validated_data.get('value', None)
        query_columns = [ConfigItemTypeAttributeModel.value_type]
        ci_type_attribute = ci_type_attribute_manager.get_by_id(
            ci_type_attribute_id, query_columns=query_columns, raise_error=True
        ).first()
        value_type = ci_type_attribute.value_type.value
        value_schema = ci_value_update_schema_mapping[value_type]
        value = value_schema(value=value).value
        instance = self.get_by_ci_id_and_ci_type_attribute_id(
            ci_id, ci_type_attribute_id=ci_type_attribute_id, value_type=value_type, raise_error=True
        ).first()
        setattr(instance, 'value', value)

    def batch_delete_by_ci_id(self, ci_id_list: t.List[int]) -> None:
        """ ???????????????id??????????????????????????????

        @param ci_id_list: ?????????id??????
        @return: None
        """
        from project.common.manager.config_item import ConfigItemManager

        ci_manager = ConfigItemManager(self.service, session=self.session)
        for value_type in ci_manager.batch_get_ci_value_types_by_id(ci_id_list):
            ci_value_manager_cls = ci_value_manager_mapping[value_type]
            ci_value_manager = ci_value_manager_cls(self.service, session=self.session)
            ci_value_manager.batch_delete_by_ci_id(ci_id_list)

    def delete_by_ci_id(self, ci_id: int) -> None:
        """ ???????????????id??????????????????

        @param ci_id: ?????????id
        @return: None
        """
        self.batch_delete_by_ci_id([ci_id])
