#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeValueType

from .config_item_bool_value.create import CreateConfigItemBoolValueParams
from .config_item_bool_value.update import UpdateConfigItemBoolValueParams
from .config_item_bool_value.getall import ListConfigItemBoolValueSchema
from .config_item_date_value.create import CreateConfigItemDateValueParams
from .config_item_date_value.update import UpdateConfigItemDateValueParams
from .config_item_date_value.getall import ListConfigItemDateValueSchema
from .config_item_datetime_value.create import CreateConfigItemDatetimeValueParams
from .config_item_datetime_value.update import UpdateConfigItemDatetimeValueParams
from .config_item_datetime_value.getall import ListConfigItemDatetimeValueSchema
from .config_item_float_value.create import CreateConfigItemFloatValueParams
from .config_item_float_value.update import UpdateConfigItemFloatValueParams
from .config_item_float_value.getall import ListConfigItemFloatValueSchema
from .config_item_int_value.create import CreateConfigItemIntValueParams
from .config_item_int_value.update import UpdateConfigItemIntValueParams
from .config_item_int_value.getall import ListConfigItemIntValueSchema
from .config_item_ipv4_value.create import CreateConfigItemIPV4ValueParams
from .config_item_ipv4_value.update import UpdateConfigItemIPV4ValueParams
from .config_item_ipv4_value.getall import ListConfigItemIPV4ValueSchema
from .config_item_json_value.create import CreateConfigItemJsonValueParams
from .config_item_json_value.update import UpdateConfigItemJsonValueParams
from .config_item_json_value.getall import ListConfigItemJsonValueSchema
from .config_item_text_value.create import CreateConfigItemTextValueParams
from .config_item_text_value.update import UpdateConfigItemTextValueParams
from .config_item_text_value.getall import ListConfigItemTextValueSchema
from .config_item_textarea_value.create import CreateConfigItemTextareaValueParams
from .config_item_textarea_value.update import UpdateConfigItemTextareaValueParams
from .config_item_textarea_value.getall import ListConfigItemTextareaValueSchema
from .config_item_time_value.create import CreateConfigItemTimeValueParams
from .config_item_time_value.update import UpdateConfigItemTimeValueParams
from .config_item_time_value.getall import ListConfigItemTimeValueSchema
from .config_item_timezone_value.create import CreateConfigItemTimezoneValueParams
from .config_item_timezone_value.update import UpdateConfigItemTimezoneValueParams
from .config_item_timezone_value.getall import ListConfigItemTimezoneValueSchema
from .config_item_user_value.create import CreateConfigItemUserValueParams
from .config_item_user_value.update import UpdateConfigItemUserValueParams
from .config_item_user_value.getall import ListConfigItemUserValueSchema

ci_value_create_schema_mapping = {
    ConfigItemTypeAttributeValueType.BOOL.value: CreateConfigItemBoolValueParams,
    ConfigItemTypeAttributeValueType.DATE.value: CreateConfigItemDateValueParams,
    ConfigItemTypeAttributeValueType.DATETIME.value: CreateConfigItemDatetimeValueParams,
    ConfigItemTypeAttributeValueType.FLOAT.value: CreateConfigItemFloatValueParams,
    ConfigItemTypeAttributeValueType.INT.value: CreateConfigItemIntValueParams,
    ConfigItemTypeAttributeValueType.IPV4.value: CreateConfigItemIPV4ValueParams,
    ConfigItemTypeAttributeValueType.JSON.value: CreateConfigItemJsonValueParams,
    ConfigItemTypeAttributeValueType.TEXT.value: CreateConfigItemTextValueParams,
    ConfigItemTypeAttributeValueType.TEXTAREA.value: CreateConfigItemTextareaValueParams,
    ConfigItemTypeAttributeValueType.TIME.value: CreateConfigItemTimeValueParams,
    ConfigItemTypeAttributeValueType.TIMEZONE.value: CreateConfigItemTimezoneValueParams,
    ConfigItemTypeAttributeValueType.USER.value: CreateConfigItemUserValueParams
}

ci_value_update_schema_mapping = {
    ConfigItemTypeAttributeValueType.BOOL.value: UpdateConfigItemBoolValueParams,
    ConfigItemTypeAttributeValueType.DATE.value: UpdateConfigItemDateValueParams,
    ConfigItemTypeAttributeValueType.DATETIME.value: UpdateConfigItemDatetimeValueParams,
    ConfigItemTypeAttributeValueType.FLOAT.value: UpdateConfigItemFloatValueParams,
    ConfigItemTypeAttributeValueType.INT.value: UpdateConfigItemIntValueParams,
    ConfigItemTypeAttributeValueType.IPV4.value: UpdateConfigItemIPV4ValueParams,
    ConfigItemTypeAttributeValueType.JSON.value: UpdateConfigItemJsonValueParams,
    ConfigItemTypeAttributeValueType.TEXT.value: UpdateConfigItemTextValueParams,
    ConfigItemTypeAttributeValueType.TEXTAREA.value: UpdateConfigItemTextareaValueParams,
    ConfigItemTypeAttributeValueType.TIME.value: UpdateConfigItemTimeValueParams,
    ConfigItemTypeAttributeValueType.TIMEZONE.value: UpdateConfigItemTimezoneValueParams,
    ConfigItemTypeAttributeValueType.USER.value: UpdateConfigItemUserValueParams
}

ci_value_getall_schema_mapping = {
    ConfigItemTypeAttributeValueType.BOOL.value: ListConfigItemBoolValueSchema,
    ConfigItemTypeAttributeValueType.DATE.value: ListConfigItemDateValueSchema,
    ConfigItemTypeAttributeValueType.DATETIME.value: ListConfigItemDatetimeValueSchema,
    ConfigItemTypeAttributeValueType.FLOAT.value: ListConfigItemFloatValueSchema,
    ConfigItemTypeAttributeValueType.INT.value: ListConfigItemIntValueSchema,
    ConfigItemTypeAttributeValueType.IPV4.value: ListConfigItemIPV4ValueSchema,
    ConfigItemTypeAttributeValueType.JSON.value: ListConfigItemJsonValueSchema,
    ConfigItemTypeAttributeValueType.TEXT.value: ListConfigItemTextValueSchema,
    ConfigItemTypeAttributeValueType.TEXTAREA.value: ListConfigItemTextareaValueSchema,
    ConfigItemTypeAttributeValueType.TIME.value: ListConfigItemTimeValueSchema,
    ConfigItemTypeAttributeValueType.TIMEZONE.value: ListConfigItemTimezoneValueSchema,
    ConfigItemTypeAttributeValueType.USER.value: ListConfigItemUserValueSchema
}
