import pytest
from fastapi import status


class TestRoomTypePostEndpoint:
    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            ({"title": "Deluxe Suite"}, status.HTTP_201_CREATED),
            ({"title": "Standard Room"}, status.HTTP_201_CREATED),
        ]
    )
    def test_create_room_type(self, http_client, payload, expected_status):
        response = http_client.post("/room_types/", json=payload)
        assert response.status_code == expected_status
        assert response.json().get("title") == payload["title"]

    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            ({}, status.HTTP_422_UNPROCESSABLE_ENTITY),
            ({"title": "A"}, status.HTTP_400_BAD_REQUEST),

        ]
    )
    def test_create_room_type_fail(self, http_client, payload, expected_status):
        response = http_client.post("/room_types/", json=payload)
        assert response.status_code == expected_status
        assert response.json().get("title") is None

    @pytest.mark.parametrize(
        "room_type_id, payload, expected_status",
        [
            (1, {"title": "Updated Suite"}, status.HTTP_200_OK)
        ]
    )
    def test_put_room_type(self, http_client, room_type_id, payload, expected_status):
        response = http_client.put(f"/room_types/{room_type_id}/", json=payload)
        assert response.status_code == expected_status
        assert response.json().get("title") == payload["title"]

    @pytest.mark.parametrize(
        "room_type_id, payload, expected_status",
        [
            (999, {"title": "Nonexistent Room"}, status.HTTP_404_NOT_FOUND),
            (1, {}, status.HTTP_422_UNPROCESSABLE_ENTITY),
            (1, {"name": "test"}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ]
    )
    def test_delete_room_type_fail(self, http_client, room_type_id, payload, expected_status):
        response = http_client.put(f"/room_types/{room_type_id}/", json=payload)
        assert response.status_code == expected_status
        assert response.json().get("title") is None


