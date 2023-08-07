from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin
from src.database import db_config, provide_transaction
from src.handlers import get_average_time_between_pull_request_events, list_repositories, get_number_of_events_per_type

app = Litestar(
    route_handlers=[list_repositories, get_average_time_between_pull_request_events, get_number_of_events_per_type],
    dependencies={"transaction": provide_transaction},
    plugins=[
        SQLAlchemyPlugin(db_config),
    ],
)
