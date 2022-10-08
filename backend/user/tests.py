from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class TestUser(APITestCase):
    """
    유저 유닛 테스트
    - 회원가입

    """

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_success_user_sign_up(self):
        """
        회원가입 성공 테스트
        :return:
        """
        sign_up_data = {
            "username": "adam",
            "email": "adam2@naver.com",
            "password1": "1234@1234",
            "password2": "1234@1234",
            "age": 25,
            "phone_number": "010-4212-3212",
            "gender": "m",
        }

        res = self.client.post(
            "/users/signup/",
            sign_up_data,
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual("access_token" in res.data, True)
        self.assertEqual("refresh_token" in res.data, True)
        self.assertEqual(res.data.get("user"), {"pk": 1, "email": "adam2@naver.com"})
