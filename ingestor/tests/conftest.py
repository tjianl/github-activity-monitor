import pytest
from testcontainers.postgres import PostgresContainer
from src.postgres_functions import DBEngine


@pytest.fixture(scope="module", autouse=True)
def db_engine():
    # Will be executed before the first test
    postgres_container = PostgresContainer(
        "postgres:15.3")

    # Start the container
    postgres_container.start()

    # Fireup the alchemy engine with the uri of the container
    db_engine = DBEngine(postgres_container.get_connection_url())

    # Perform tests, and make db_engine available
    yield db_engine

    # Will be executed after the last test
    db_engine.session.close()
    postgres_container.stop()
