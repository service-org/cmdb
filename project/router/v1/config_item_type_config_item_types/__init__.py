#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_core.core.as_router import ApiRouter

from . import create
from . import getall
from . import update
from . import delete


router = ApiRouter(__name__)

router.include_router(create.router)
router.include_router(getall.router)
router.include_router(update.router)
router.include_router(delete.router)

