#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from project.models.v1.config_item_type_attribute import ConfigItemTypeAttributeValueType

from .config_item_bool_value import ConfigItemBoolValueModel
from .config_item_date_value import ConfigItemDateValueModel
from .config_item_datetime_value import ConfigItemDatetimeValueModel
from .config_item_float_value import ConfigItemFloatValueModel
from .config_item_int_value import ConfigItemIntValueModel
from .config_item_ipv4_value import ConfigItemIPV4ValueModel
from .config_item_json_value import ConfigItemJsonValueModel
from .config_item_text_value import ConfigItemTextValueModel
from .config_item_textarea_value import ConfigItemTextareaValueModel
from .config_item_time_value import ConfigItemTimeValueModel
from .config_item_timezone_value import ConfigItemTimezoneValueModel
from .config_item_user_value import ConfigItemUserValueModel

ci_value_model_mapping = {
    ConfigItemTypeAttributeValueType.BOOL.value: ConfigItemBoolValueModel,
    ConfigItemTypeAttributeValueType.DATE.value: ConfigItemDateValueModel,
    ConfigItemTypeAttributeValueType.DATETIME.value: ConfigItemDatetimeValueModel,
    ConfigItemTypeAttributeValueType.FLOAT.value: ConfigItemFloatValueModel,
    ConfigItemTypeAttributeValueType.INT.value: ConfigItemIntValueModel,
    ConfigItemTypeAttributeValueType.IPV4.value: ConfigItemIPV4ValueModel,
    ConfigItemTypeAttributeValueType.JSON.value: ConfigItemJsonValueModel,
    ConfigItemTypeAttributeValueType.TEXT.value: ConfigItemTextValueModel,
    ConfigItemTypeAttributeValueType.TEXTAREA.value: ConfigItemTextareaValueModel,
    ConfigItemTypeAttributeValueType.TIME.value: ConfigItemTimeValueModel,
    ConfigItemTypeAttributeValueType.TIMEZONE.value: ConfigItemTimezoneValueModel,
    ConfigItemTypeAttributeValueType.USER.value: ConfigItemUserValueModel,
}
