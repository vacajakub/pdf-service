import asyncio

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from psycopg_pool import AsyncConnectionPool
from pydantic_settings import BaseSettings
from starlette.datastructures import State

from .config import get_settings


def get_db_connection_str(settings: BaseSettings, read_only=False) -> str:
    return f"""
            dbname={settings.db_slave_name if read_only else settings.db_master_name}
            user={settings.db_user}
            password={settings.db_password}
            host={settings.db_host}
            port={settings.db_slave_port if read_only else settings.db_master_port}
           """


def create_db_connection(settings: BaseSettings, read_only=False) -> AsyncConnectionPool:
    return AsyncConnectionPool(conninfo=get_db_connection_str(settings, read_only))


class AppState(State):
    settings: BaseSettings

    db_master: AsyncConnectionPool
    db_slave: AsyncConnectionPool

    async def setup(self):
        self.settings = get_settings()
        # on local docker-compose master and slave is same but in production environment it should be
        # so reads on slave, other on master
        self.db_master = create_db_connection(self.settings)
        self.db_slave = create_db_connection(self.settings, True)
        print("DB connected")

        # rabbit_broker = RabbitmqBroker(host=self.settings.rabbit_host, port=self.settings.rabbit_port)
        # rabbit_broker = RabbitmqBroker()
        # dramatiq.set_broker(rabbit_broker)
        # print("Broker set")
