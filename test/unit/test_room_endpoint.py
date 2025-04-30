# import pytest
# from fastapi import status
#
#
# class TestRoomEndpoint:
#     @pytest.mark.parametrize(
#         "path, expected_status",
#         [
#             ("/rooms/", status.HTTP_200_OK),
#             ("/test/", status.HTTP_404_NOT_FOUND),
#             ("/room_types/1", status.HTTP_200_OK),
#             ("/rooms/999/", status.HTTP_404_NOT_FOUND),
#             ("/rooms/1i/", status.HTTP_422_UNPROCESSABLE_ENTITY),
#             ("/room_types/999/", status.HTTP_404_NOT_FOUND),
#         ]
#     )
#     def test_rooms(self, http_client, path, expected_status):
#         response = http_client.get(path)
#         assert response.status_code == expected_status
