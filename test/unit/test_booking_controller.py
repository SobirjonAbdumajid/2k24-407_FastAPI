from datetime import timedelta, date

import pytest
from pytest_mock import MockerFixture

from app.api.controller.booking import BookingController
from app.api.models import Bookings
from app.api.repositories.booking import BookingRepository
from app.api.schemas.bookings import BookingSchema


@pytest.fixture
def booking_repository():
    return BookingRepository()


@pytest.fixture
def booking_controller(booking_repository):
    return BookingController(booking_repository)


@pytest.mark.asyncio
async def test_make_booking(booking_repository, booking_controller,
                            mocker: MockerFixture, get_faker):

    mocker.patch.object(booking_repository, 'get_room_price',
                        return_value=get_faker.random_int())
    random_date = get_faker.date_time()
    mock_booking = Bookings(
        room_id=get_faker.random_int(),
        user_id=get_faker.random_int(),
        check_in=random_date,
        check_out=random_date + timedelta(days=10),
        total_price=get_faker.random_int(),
        status=get_faker.lexify('??????')
    )
    mocker.patch.object(booking_repository, 'make_booking',
                        return_value=mock_booking)
    fake_date = get_faker.date_object()
    random_date = fake_date
    mock_data = BookingSchema(
        user_id=get_faker.random_int(),
        room_id=get_faker.random_int(),
        check_in=random_date,
        check_out=random_date + timedelta(days=10),
        status=get_faker.lexify('??????')
    )
    result = await booking_controller.make_booking(mock_data)
    assert result == mock_booking

