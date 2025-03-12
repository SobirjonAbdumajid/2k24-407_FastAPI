import pytest
from fastapi import status


class TestRoomTypePostEndpoint:
    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            ({"title": "Deluxe Suite"}, status.HTTP_201_CREATED),
            ({}, status.HTTP_422_UNPROCESSABLE_ENTITY),
            ({"title": "Standard Room"}, status.HTTP_201_CREATED),
            ({"title": "A"}, status.HTTP_400_BAD_REQUEST),
        ]
    )
    def test_create_room_type(self, http_client, payload, expected_status):
        response = http_client.post("/room_types/", json=payload)
        assert response.status_code == expected_status
