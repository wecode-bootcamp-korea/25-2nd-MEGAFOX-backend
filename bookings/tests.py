import jwt

from django.test      import TestCase, Client
from likes.models     import UserLikeTheater

from theaters.models  import *
from bookings.models  import *
from movies.models    import *
from users.models     import *
from megafox.settings import SECRET_KEY, ALGORITHM

class BookingTest(TestCase):
    
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
            ),
            Theater(
                id      = 2,
                name    = '동대문',
                city_id = 1
            ),
            Theater(
                id      = 3,
                name    = '신촌',
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

        Image.objects.bulk_create([
            Image(movie_id = 1, main_image_url = 'naver.com', sub_image_url = 'naver.com'),
            Image(movie_id = 2, main_image_url = 'naver.com', sub_image_url = 'naver.com')
        ])

        MovieTheater.objects.bulk_create([
            MovieTheater(
                id          = 1,
                screen_time = '2021-10-29 08:10:00',
                movie_id    = 1,
                theater_id  = 1
            )
        ])
        
        User.objects.bulk_create([
            User(
                id       = 1,
                name     = '김김김',
                email    = 'sample@test.com',
                kakao_id = '1231231'
            ),
            User(
                id       = 2,
                name     = '이이이',
                email    = 'sampleid@test.com',
                kakao_id = '1231232'
            ),
            User(
                id       = 3,
                name     = '박박박',
                email    = 'sampleemail@test.com',
                kakao_id = '1231233'
            ),
            User(
                id       = 4,
                name     = '최최최',
                email    = 'sampletest@test.com',
                kakao_id = '1231234'
            ),
        ])
        
        UserLikeTheater.objects.bulk_create([
            UserLikeTheater(
                id         = 1,
                theater_id = 1,
                user_id    = 1
            ),
            UserLikeTheater(
                id         = 2,
                theater_id = 2,
                user_id    = 1
            )
        ])

        Booking.objects.bulk_create([
            Booking(
                id               = 1,
                total_price      = 20000,
                adult            = 2,
                teenager         = 0,
                kid              = 0,
                movie_theater_id = 1,
                user_id          = 1,
            ),
            Booking(
                id               = 2,
                total_price      = 20000,
                adult            = 2,
                teenager         = 0,
                kid              = 0,
                movie_theater_id = 1,
                user_id          = 4
            ),
        ])

    def tearDown(self):
        Booking.objects.all().delete()
        MovieTheater.objects.all().delete()
        Theater.objects.all().delete()
        UserLikeTheater.objects.all().delete()
        City.objects.all().delete()
        Image.objects.all().delete()
        User.objects.all().delete()
        Movie.objects.all().delete()

    def test_booking_info_get_succcess(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.get('/booking', **{'HTTP_Authorization' : access_token})

        self.assertEqual(response.json(),
        {'results' : [{
            'id'           : 1,
            'movie_image'  : 'naver.com',
            'theater'      : '강남',
            'movie_name'   : '베놈 2',
            'screen_time'  : '2021.10.29 Friday 08:10',
            'people'       : {
                "adult" : 2,
                "teenager" : 0,
                "kid" : 0
            },
            'booking_date' : '2021.10.28'
            }]
        })

        self.assertEqual(response.status_code, 200)

    def test_reserve_post_success(self):
        access_token = jwt.encode({'id' : 2}, SECRET_KEY, ALGORITHM)
        client       = Client()

        booking = {
            'user_id' : 2,
            'movie_theater_id' : 1,
            'adult' : 2,
            'teenager' : 1,
            'kid' : 1
        }

        response = client.post('/booking/reserve', **{'HTTP_Authorization' : access_token, 'data' : booking}, content_type='application/json')

        self.assertEqual(response.json(),
        {
            'message' : 'SUCCESS'
        })
        self.assertEqual(response.status_code, 201)

    def test_reserve_post_key_error_failure(self):
        access_token = jwt.encode({'id' : 2}, SECRET_KEY, ALGORITHM)
        client       = Client()

        booking = {
            'user_id' : 2,
            'adult' : 2,
            'teenager' : 1,
            'kid' : 1
        }

        response = client.post('/booking/reserve', **{'HTTP_Authorization' : access_token, 'data' : booking}, content_type='application/json')

        self.assertEqual(response.json(),
        {
            'message' : 'KEY_ERROR'
        })
        self.assertEqual(response.status_code, 400)

    def test_reserve_post_movie_theater_does_not_exist_failure(self):
        access_token = jwt.encode({'id' : 2}, SECRET_KEY, ALGORITHM)
        client       = Client()

        booking = {
            'movie_theater_id' : 5,
            'adult'            : 2,
            'teenager'         : 1,
            'kid'              : 1
        }

        response = client.post('/booking/reserve', **{'HTTP_Authorization' : access_token, 'data' : booking}, content_type='application/json')

        self.assertEqual(response.json(),
        {
            'message' : 'DOES_NOT_EXIST'
        })
        self.assertEqual(response.status_code, 404)

    def test_reserve_get_success(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.get('/booking/reserve?date=2021-10-29', **{'HTTP_Authorization' : access_token})

        self.assertEqual(response.json(),
        {
            "result": {
                "movie_list": [
                    {
                        "movie_id"     : 1,
                        "movie_name"   : '베놈 2',
                        "age_rate"     : '15세',
                        "is_userlike"  : False,
                        "is_available" : True,
                        "poster"       : 'naver.com'
                    },
                    {
                        "movie_id"     : 2,
                        "movie_name"   : '듄',
                        "age_rate"     : '15세',
                        "is_userlike"  : False,
                        "is_available" : False,
                        "poster"       : 'naver.com'
                    },
                ],
                "theater_list" : [
                    {
                        "city_id"        : 0,
                        "city_name"      : "선호극장",
                        "theater_count"  : 2,
                        "theater" : [
                            {
                                "theater_id"  : 1,
                                "theater_name": "강남"
                            },
                            {
                                "theater_id"  : 2,
                                "theater_name": "동대문"
                            }
                        ]
                    },
                    {
                        "city_id"        : 1,
                        "city_name"      : "서울",
                        "theater_count"  : 3,
                        "theater" : [
                            {
                                "theater_id"  : 1,
                                "theater_name": "강남"
                            },
                            {
                                "theater_id"  : 2,
                                "theater_name": "동대문"
                            },
                            {
                                "theater_id"  : 3,
                                "theater_name": "신촌"
                            }
                        ]
                    }
                ],
                "movie_info" : [
                    {
                        "movie_id"           : 1,
                        "movie_name"         : "베놈 2",
                        "movie_theater_id"   : 1,
                        "movie_theater_name" : "강남",
                        "start_time"         : "08:10",
                        "end_time"           : "10:10"
                    }
                ]
            }
        })

        self.assertEqual(response.status_code, 200)

    def test_reserve_get_movie_theater_does_not_exist_failure(self):
        access_token = jwt.encode({'id' : 4}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.get('/booking/reserve?date=2021-12-28', **{'HTTP_Authorization' : access_token})

        self.assertEqual(response.json(),
        {
            'message' : 'MOVIE_OR_THEATER_DOES_NOT_EXIST'
        })
        self.assertEqual(response.status_code, 404)
