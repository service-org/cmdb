#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from project.router import v1
from project.service import Service
from service_core.core.as_router import ApiRouter

router = ApiRouter(__name__)
router.include_router(v1.router)

service = Service()
service.include_router(router)
