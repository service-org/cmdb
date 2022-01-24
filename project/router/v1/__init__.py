#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.core.as_router import ApiRouter

from . import relation
from . import config_item
from . import config_item_type
from . import config_item_type_group
from . import config_item_type_attribute
from . import config_item_type_attribute_group
from . import config_item_type_config_item_types

router = ApiRouter(__name__)

router.include_router(relation.router)
router.include_router(config_item.router)
router.include_router(config_item_type.router)
router.include_router(config_item_type_group.router)
router.include_router(config_item_type_attribute.router)
router.include_router(config_item_type_attribute_group.router)
router.include_router(config_item_type_config_item_types.router)
