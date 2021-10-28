import jwt

from django.test   import TestCase, Client
from unittest.mock import MagicMock, patch

from users.models     import User
from bookings.models  import Booking
from theaters.models  import *
from movies.models    import *
from megafox.settings import SECRET_KEY, ALGORITHM

class KakaoSigninTest(TestCase):
    def setUp(self):
        City.objects.create(
            id   = 1,
            name = '서울'
        )

        Theater.objects.bulk_create([
            Theater(
                id      = 1,
                name    = '강남',
                city_id = 1
            )
        ])

        Movie.objects.bulk_create([
            Movie(
                id             = 1,
                ko_name        = '베놈 2',
                eng_name       = 'venom 2',
                release_date   = '2021-10-10',
                close_date     = '2022-01-01',
                screen_type    = '2D',
                director       = '앤디 서키스',
                genre          = '액션',
                running_time   = 120,
                age_rate       = '15세',
                actor          = '톰 하디, 우디 해럴슨',
                total_audience = 12000000,
                description    = 'aaaaaaaaaaaa'
            ),
            Movie(
                id             = 2,
                ko_name        = '듄',
                eng_name       = 'Dune',
                release_date   = '2021-10-10',
                close_date     = '2022-01-01',
                screen_type    = '2D',
                director       = '드니 빌뇌브',
                genre          = '액션',
                running_time   = 120,
                age_rate       = '15세',
                actor          = '티머시 섈러메이, 젠데이아',
                total_audience = 12000000,
                description    = 'aaaaaaaaaaaa'
            )
        ])

        MovieTheater.objects.bulk_create([
            MovieTheater(
                id          = 1,
                screen_time = '2021-10-29 08:10:00',
                movie_id    = 1,
                theater_id  = 1
            )
        ])
        
        User.objects.create(
            id       = 1,
            name     = "홍길동",
            email    = "gildonghong@sample.com",
            kakao_id = "100010000",
            point    = 0
        )

        Booking.objects.bulk_create([
            Booking(
                id               = 1,
                total_price      = 20000,
                adult            = 2,
                teenager         = 0,
                kid              = 0,
                movie_theater_id = 1,
                user_id          = 1,
            )
        ])

    def tearDown(self):
        Booking.objects.all().delete()
        MovieTheater.objects.all().delete()
        Theater.objects.all().delete()
        City.objects.all().delete()
        Image.objects.all().delete()
        User.objects.all().delete()
        Movie.objects.all().delete()

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

    def test_login_check_get_success(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.get('/users/info', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.json(),
        {
            "result": {
                "user_id" : 1,
                "point"   : 0,
                "name"    : "홍길동",
                "booking" : [{
                    "count"  : 1,
                    "detail" : {
                        "booking_id" : 1
                    }
                }]
            }
        })

        self.assertEqual(response.status_code, 200)