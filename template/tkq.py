import taskiq_fastapi
from taskiq import InMemoryBroker, ZeroMQBroker

from template.settings import settings

broker = ZeroMQBroker()

if settings.environment.lower() == "pytest":
    broker = InMemoryBroker()

taskiq_fastapi.init(
    broker,
    "template.web.application:get_app",
)
