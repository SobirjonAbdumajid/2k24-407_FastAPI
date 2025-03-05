import random

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from faker import Faker

from app.core.models.base import Base
from app.core.settings import Settings, get_settings
from app.server.app import create_app
from app.api.models.rooms import Rooms, RoomsType, RoomsStatus
from app.api.models.users import Users
from app.api.models.bookings import Bookings
from app.api.models.feedback import FeedBack
from app.api.models.payments import Payments

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


@pytest.fixture(autouse=True)
def feed_mock_data(get_faker, db_session):
    faker = get_faker

    mock_rooms_status = [RoomsStatus(title=faker.lexify('??????')) for _ in range(5)]
    mock_rooms_types = [RoomsType(title=faker.lexify('??????')) for _ in range(5)]

    db_session.add_all(mock_rooms_status)
    db_session.add_all(mock_rooms_types)
    db_session.commit()

    rooms_status_list = db_session.query(RoomsStatus).all()
    rooms_types_list = db_session.query(RoomsType).all()

    mock_rooms = [Rooms(
        room_number=faker.random_number(),
        room_type=random.choice(rooms_types_list).id,
        price=faker.pyfloat(min_value=5, max_value=100, positive=True),
        status=random.choice(rooms_status_list).id,
    ) for _ in range(5)]

    db_session.add_all(mock_rooms)
    db_session.commit()
    rooms_list = db_session.query(Rooms).all()

    mock_users = [Users(
        password=faker.password(),
        username=faker.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        is_staff=faker.boolean(),
        is_active=faker.boolean(),
        is_superuser=faker.boolean(),
        created_at=faker.date_time(),
    ) for _ in range(5)]

    db_session.add_all(mock_users)
    db_session.commit()

    users_list = db_session.query(Users).all()
    mock_bookings = [Bookings(
        user_id=random.choice(users_list).id,
        room_id=random.choice(rooms_list).id,
        check_in=faker.date_time(),
        check_out=faker.date_time(),
        total_price=faker.pyfloat(min_value=5, max_value=100, positive=True),
        status=random.choice(rooms_status_list).id,
    ) for _ in range(5)]

    db_session.add_all(mock_bookings)
    db_session.commit()

    bookings_list = db_session.query(Bookings).all()

    mock_feedback = [FeedBack(
        user_id=random.choice(users_list).id,
        room_id=random.choice(rooms_list).id,
        comment=faker.text(max_nb_chars=20),
    ) for _ in range(5)]

    db_session.add_all(mock_feedback)
    db_session.commit()

    mock_payments = [Payments(
        booking_id=random.choice(bookings_list).id,
        payment_date=faker.date_time(),
        amount=faker.pyfloat(min_value=5, max_value=100, positive=True),
        payment_method=random.choice(['cash', 'credit']),
        status=random.choice(rooms_status_list).id,
    ) for _ in range(5)]

    db_session.add_all(mock_payments)
    db_session.commit()


@pytest.fixture
def get_faker() -> Faker:
    return Faker()


@pytest.fixture(scope="session")
def http_client():
    print('HTTP client started successfully\n')
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
