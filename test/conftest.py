import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.core.models.base import Base
from app.core.settings import Settings, get_settings
from app.server.app import create_app

load_dotenv('.env.test')
settings: Settings = get_settings()

engine = create_engine('postgresql+psycopg2://' + settings.GET_POSTGRES_URL)

TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope='session', autouse=True)
def db_session():
    print('Session started successfully\n')
    session = TestingSession()
    yield session
    session.close()
    print('Session ended successfully\n')


@pytest.fixture(scope='session', autouse=True)
def set_up_db():
    print('Setting up DB\n')
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    print('Setting up DB done')


@pytest.fixture(scope='session')
def http_client():
    print('HTTP client started successfully\n')
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def test_smth(http_client):
    print('Testing smth function\n')
    assert True
    print('Testing smth done\n')
