from http.client import responses

import pytest
from fastapi import status
from datetime import datetime


class TestEndpoints:
    @pytest.mark.parametrize(
        "path, expected",
        [
            ('/rooms', status.HTTP_200_OK),
            ('/rooms/', status.HTTP_200_OK),
        ]
    )
    def test_get_rooms(self, http_client, path, expected):
        response = http_client.get(path)
        assert response.status_code == expected

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        'path, expected',
        [
            ('/rooms', status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_get_rooms_failed(self, http_client, path, expected):
        response = http_client.get(path)
        assert response.status_code == expected

    @pytest.mark.parametrize(
        'room_id, expected',
        [
            (1, status.HTTP_200_OK),
            (5, status.HTTP_200_OK),
            (999, status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_get_room_by_id_success(self, http_client, room_id, expected):
        response = http_client.get(f'/rooms/{room_id}/')
        assert response.status_code == expected

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        'room_id, expected',
        [
            ('1', status.HTTP_422_UNPROCESSABLE_ENTITY),
        ]
    )
    def test_get_room_by_id_failed(self, http_client, room_id, expected):
        response = http_client.get(f'/rooms/{room_id}/')
        assert response.status_code == expected

    @pytest.mark.parametrize(
        'data, expected, status_code',
        [
            (
                    {
                        "user_id": 1,
                        "room_id": 1,
                        "check_in": "2025-03-11",
                        "check_out": "2025-03-11",
                        "status": "string"
                    },
                    {
                        "user_id": 1,
                        "room_id": 1,
                        "check_in": "2025-03-11",
                        "check_out": "2025-03-11",
                        "status": "string",
                    },
                    status.HTTP_201_CREATED
            ),
        ]
    )
    def test_post_booking_success(self, http_client, data, expected, status_code):
        response = http_client.post('booking/', json=data)
        assert response.status_code == status_code
        response_body = response.json()
        assert response_body['user_id'] == data['user_id']
        assert response_body['room_id'] == data['room_id']
        assert str(datetime.fromisoformat(response_body['check_in']).date()) == data['check_in']
        assert str(datetime.fromisoformat(response_body['check_out']).date()) == data['check_out']
        assert response_body['status'] == data['status']

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        'data, expected, status_code',
        [
            (
                    {
                        'user_id': 1,
                    },
                    {
                        'user_id': 1,
                    },
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        ]
    )
    def test_post_booking_failed(self, http_client, data, expected, status_code):
        response = http_client.post('booking/', json=data)
        assert response.status_code == status_code
