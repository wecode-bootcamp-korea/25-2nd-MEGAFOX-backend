import jwt

from django.test      import TestCase, Client

from reviews.models   import Review, ReviewViewingPoint, ViewingPoint
from theaters.models  import Theater, City, MovieTheater
from bookings.models  import Booking
from movies.models    import Movie
from users.models     import User
from megafox.settings import SECRET_KEY, ALGORITHM

class ReviewTest(TestCase):
    def setUp(self):
        ViewingPoint.objects.bulk_create([
            ViewingPoint(
                id   = 1,
                name = '연출'
            ),
            ViewingPoint(
                id   = 2,
                name = '스토리' 
            ),
            ViewingPoint(
                id   = 3,
                name = '영상미'
            ),
            ViewingPoint(
                id   = 4,
                name = '배우'
            ),
            ViewingPoint(
                id   = 5,
                name = 'OST'
            ),
        ])

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
            ),
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
                screen_time = '2021-10-20 08:10:00',
                movie_id    = 1,
                theater_id  = 1
            ),
            MovieTheater(
                id          = 2,
                screen_time = '2021-10-20 10:10:00',
                movie_id    = 1,
                theater_id  = 1
            ),
            MovieTheater(
                id          = 3,
                screen_time = '2021-10-20 12:10:00',
                movie_id    = 1,
                theater_id  = 1
            ),
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

        Booking.objects.bulk_create([
            Booking(
                id               = 1,
                total_price      = 20000,
                adult            = 2,
                teenager         = 0,
                kid              = 0,
                movie_theater_id = 1,
                user_id          = 1
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

        Review.objects.bulk_create([
            Review(
                id       = 1,
                rating   = 3,
                body     = '별로 재미 없음',
                movie_id = 1,
                user_id  = 1
            ),
            Review(
                id       = 2,
                rating   = 9,
                body     = '완전 재미 있음',
                movie_id = 1,
                user_id  = 2
            ),
            Review(
                id       = 3,
                rating   = 5,
                body     = '그냥 그래요',
                movie_id = 1,
                user_id  = 3
            )
        ])

        ReviewViewingPoint.objects.bulk_create([
            ReviewViewingPoint(
                id               = 1,
                review_id        = 1,
                viewing_point_id = 1
            ),
            ReviewViewingPoint(
                id               = 2,
                review_id        = 1,
                viewing_point_id = 2
            ),
            ReviewViewingPoint(
                id               = 3,
                review_id        = 2,
                viewing_point_id = 3,
            ),
            ReviewViewingPoint(
                id               = 4,
                review_id        = 2,
                viewing_point_id = 4,
            ),
            ReviewViewingPoint(
                id               = 5,
                review_id        = 3,
                viewing_point_id = 5,
            ),
            ReviewViewingPoint(
                id               = 6,
                review_id        = 3,
                viewing_point_id = 1,
            ),
        ])
    
    def tearDown(self):
        ReviewViewingPoint.objects.all().delete()
        Review.objects.all().delete()
        Booking.objects.all().delete()
        User.objects.all().delete()
        MovieTheater.objects.all().delete()
        Movie.objects.all().delete()
        Theater.objects.all().delete()
        City.objects.all().delete()
        ViewingPoint.objects.all().delete()

    def test_review_get_movies_does_not_exist(self):
        client   = Client()
        response = client.get('/review/comment?movieNo=12321&offset=0&limit=2&sort=like')

        self.assertEqual(response.json(), 
        {
            "message": "DOES_NOT_EXIST"
        })
        self.assertEqual(response.status_code, 404)
    
    def test_review_get_value_error(self):
        client   = Client()
        response = client.get('/review/comment?movieNo=1&offset=asd&limit=2&sort=like')

        self.assertEqual(response.json(),
        {
            "message": "VALUE_ERROR"
        })
        self.assertEqual(response.status_code, 400)

    def test_review_get_value_error(self):
        client   = Client()
        response = client.get('/review/comment?movieNo=1&offset=0&limit=2&sort=asdlkajsdk')

        self.assertEqual(response.json(),
        {
            "message": "KEY_ERROR"
        })
        self.assertEqual(response.status_code, 400)
    
    def test_review_get_success(self):
        client = Client()
        response = client.get('/review/comment?movieNo=1&offset=0&limit=3&sort=rating', content_type='application/json')
        self.assertEqual(response.json(),
        {
            "count"   : 3,
            "results" : [
                {
                    "review_id" : 2,
                    "user_id"   : "sample**",
                    "rating"    : 9,
                    "viewing_points" : [
                        {
                            "id"  : 3,
                            "name": "영상미"
                        },
                        {
                            "id"  : 4,
                            "name": "배우"
                        }
                    ],
                    "body"       : "완전 재미 있음",
                    "like_count" : 0
                },
                {
                    "review_id" : 3,
                    "user_id"   : "sampleema**",
                    "rating" : 5,
                    "viewing_points" : [
                        {
                            "id"  : 5,
                            "name": "OST"
                        },
                        {
                            "id"  : 1,
                            "name": "연출"
                        }
                    ],
                    "body"       : "그냥 그래요",
                    "like_count" : 0
                },
                {
                    "review_id" : 1,
                    "user_id"   : "samp**",
                    "rating"    : 3,
                    "viewing_points" : [
                        {
                            "id"  : 1,
                            "name": "연출"
                        },
                        {
                            "id"  : 2,
                            "name": "스토리"
                        }
                    ],
                    "body"       : "별로 재미 없음",
                    "like_count" : 0
                },
            ]
        })

        self.assertEqual(response.status_code, 200)

    def test_review_post_success(self):
        access_token = jwt.encode({'id' : 4}, SECRET_KEY, ALGORITHM)
        client       = Client()

        review = {
            "rating"         : 10,
            "body"           : "완전 재밌어요",
            "viewing_points" : [1]
        }
        response = client.post('/review/comment?movieNo=1', **{'HTTP_Authorization' : access_token, 'data' : review}, content_type='application/json')

        self.assertEqual(response.json(), 
        {
            'message' : 'SUCCESS'
        })
        self.assertEquals(response.status_code, 201)

    def test_review_post_fail_key_error(self):
        access_token = jwt.encode({'id' : 4}, SECRET_KEY, ALGORITHM)
        client       = Client()

        review = {
            "body"   : "완전 재밌어요",
            "viewing_points" : [1]
        }

        response = client.post('/review/comment?movieNo=1', **{'HTTP_Authorization' : access_token, 'data' : review}, content_type='application/json')
        
        self.assertEqual(response.json(), 
        {
            'message' : 'KEY_ERROR'
        })
        self.assertEquals(response.status_code, 400)
    
    def test_review_post_fail_booking_does_not_exist(self):
        access_token = jwt.encode({'id' : 2}, SECRET_KEY, ALGORITHM)
        client       = Client()

        review = {
            "rating" : 9,
            "body"   : "완전 재밌어요",
            "viewing_points" : [1]
        }

        response = client.post('/review/comment?movieNo=1', **{'HTTP_Authorization' : access_token, 'data' : review}, content_type='application/json')

        self.assertEqual(response.json(), 
        {
            'message' : 'DOES_NOT_EXIST'
        })
        self.assertEquals(response.status_code, 404)
    
    def test_review_delete_success(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()

        response = client.delete('/review/comment/1', **{'HTTP_Authorization' : access_token})

        self.assertEqual(response.json(), 
        {
            'message' : 'SUCCESS'
        })
        self.assertEquals(response.status_code, 200)

    def test_review_delete_review_does_not_exist(self):
        access_token = jwt.encode({'id' : 2}, SECRET_KEY, ALGORITHM)
        client       = Client()

        response = client.delete('/review/comment/1', **{'HTTP_Authorization' : access_token})

        self.assertEqual(response.json(), 
        {
            'message' : 'DOES_NOT_EXIST'
        })
        self.assertEquals(response.status_code, 404)

    def test_review_patch_success(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()

        review = {
            "rating" : 3,
            "body"   : "생각해보니까 별로네요",
            "viewing_points" : [2,3]
        }

        response = client.patch('/review/comment/1', **{'HTTP_Authorization' : access_token, 'data' : review}, content_type='application/json')

        self.assertEqual(response.json(), 
        {
            'message' : 'SUCCESS'
        })
        self.assertEquals(response.status_code, 200)
    
    def test_review_patch_fail_review_does_not_exist(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()

        review = {
            "rating" : 3,
        }

        response = client.patch('/review/comment/5', **{'HTTP_Authorization' : access_token, 'data' : review}, content_type='application/json')

        self.assertEqual(response.json(), 
        {
            'message' : 'DOES_NOT_EXIST'
        })
        self.assertEquals(response.status_code, 404)
