#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from logging import getLogger
from service_consul.core.client import ConsulClient
from service_sqlalchemy.core.dependencies import SQLAlchemy
from service_prometheus.core.dependencies import Prometheus
from service_core.core.service import Service as BaseService
from service_consul.core.dependencies import ApiSixConsulKvRegist

logger = getLogger(__name__)


class Service(BaseService):
    """ 微服务类 """

    name = 'cmdb'
    desc = '资源平台相关服务'

    # 本地测试用
    port = 8081

    prometheus = Prometheus(alias='prod')
    orm: SQLAlchemy = SQLAlchemy(alias='prod', engine_options={'echo': True})
    consul: ConsulClient = ApiSixConsulKvRegist(alias='prod')
