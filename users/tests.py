from django.test import TestCase, Client
from unittest.mock import MagicMock, patch

from users.models import User

class KakaoSigninTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = "홍길동",
            email    = "gildonghong@sample.com",
            kakao_id = "100010000"
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_kakao_signin_success(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    "id"            : "100010000",
                    "kakao_account" : {
                        "profile" : {"nickname" : "홍길동"},
                        "email"   : "gildonghong@sample.com"
                    }
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "fake_access_token"}
        response            = client.get("/users/kakao/signin", **headers)

        self.assertEqual(response.status_code, 200)

    @patch("users.views.requests")
    def test_kakao_signin_fail(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "msg": "this access token does not exist",
                    "code": -401
                }
            
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "fake_access_token2"}
        response            = client.get("/users/kakao/signin", **headers)
        
        self.assertEqual(response.status_code, 400)