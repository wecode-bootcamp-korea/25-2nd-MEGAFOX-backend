import jwt

from django.test import TestCase, Client

from users.models     import *
from movies.models    import *
from theaters.models  import *
from likes.models     import *
from reviews.models   import *

from megafox.settings import SECRET_KEY, ALGORITHM

class LikeTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([   
            User(
                id            = 1,
                email         = 'gmail@gmail.com',
                name          = 'wecode',
                point         = 100000,
                kakao_id      = 'dummy1234',
                date_of_birth = '2000-01-01',
                phone_number  = '01015771577'
                ),
            User(
                id            = 2,
                email         = 'naver@gmail.com',
                name          = 'wecde',
                point         = 100000,
                kakao_id      = 'dmmy1234',
                date_of_birth = '2001-01-01',
                phone_number  = '01015771577'
                )
        ])

        Movie.objects.bulk_create([
            Movie(
                id             = 1,
                ko_name        = '베놈',
                eng_name       = 'venom',
                release_date   = '2021-10-10',
                close_date     = '2022-01-01',
                screen_type    = '1',
                director       = 'wecode',
                genre          = '코미디',
                running_time   = 120,
                age_rate       = '전체이용',
                actor          = '김김김, 박박박',
                total_audience = 123456,
                description    = 'aaaaaaaaaaaa'
            ),
            Movie(
                id             = 2,
                ko_name        = '베놈2',
                eng_name       = 'venom2',
                release_date   = '2021-10-12',
                close_date     = '2022-01-01',
                screen_type    = 1,
                director       = 'wecode',
                genre          = '코미디',
                running_time   = 120,
                age_rate       = '전체이용',
                actor          = '김김김, 박박박',
                total_audience = 12345,
                description    = 'cccccccc'
            ),
            Movie(
                id             = 3,
                ko_name        = '베놈3',
                eng_name       = 'venom3',
                release_date   = '2021-11-11',
                close_date     = '2022-01-01',
                screen_type    = '1',
                director       = 'wecode',
                genre          = '코미디',
                running_time   = 120,
                age_rate       = '전체이용',
                actor          = '김김김, 박박박',
                total_audience = 1234,
                description    = 'bbbbbbbb'
            )
        ])

        City.objects.create(
            id = 1, name = '서울'
        )

        Theater.objects.bulk_create([
            Theater(id = 1, city_id = 1, name = '신촌'),
            Theater(id = 2, city_id = 1, name = '압구정')
        ])

        Review.objects.bulk_create([
            Review(id = 1, user_id = 1, movie_id = 1, rating = 9, body = 'good'),
            Review(id = 2, user_id = 1, movie_id = 2, rating = 9, body = 'great'),
            Review(id = 3, user_id = 1, movie_id = 3, rating = 9, body = 'perfect'),
            Review(id = 4, user_id = 2, movie_id = 1, rating = 9, body = 'good'),
            Review(id = 5, user_id = 2, movie_id = 2, rating = 9, body = 'great'),
            Review(id = 6, user_id = 2, movie_id = 3, rating = 9, body = 'perfect')
        ])

        UserLikeMovie.objects.create(user_id = 2, movie_id = 2)
        
        UserLikeReview.objects.create(user_id = 2, review_id = 2)

        UserLikeTheater.objects.create(user_id = 2, theater_id = 2)

    def tearDown(self):
        Review.objects.all().delete()
        Theater.objects.all().delete()
        City.objects.all().delete()
        User.objects.all().delete()
        Movie.objects.all().delete()

    def test_user_like_movie_post_like_success(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.post('/like/movie/1', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'success'})

    def test_user_like_movie_post_like_delete_success(self):
        access_token = jwt.encode({'id' : 2}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.post('/like/movie/2', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'deleted'})

    def test_user_like_movie_does_not_exist(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.post('/like/movie/5', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message' : 'movie does not exist'})

    def test_user_like_review_post_like_success(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.post('/like/review/1', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'success'})

    def test_user_like_review_post_like_delete_success(self):
        access_token = jwt.encode({'id' : 2}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.post('/like/movie/2', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'deleted'})

    def test_user_like_review_does_not_exist(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.post('/like/review/10', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message' : 'review does not exist'})
    
    def test_user_like_theater_post_like_success(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.post('/like/theater/1', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'success'})

    def test_user_like_theater_post_like_delete_success(self):
        access_token = jwt.encode({'id' : 2}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.post('/like/movie/2', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'deleted'})

    def test_user_like_theater_does_not_exist(self):
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
        client       = Client()
        response     = client.post('/like/theater/5', **{'HTTP_Authorization' : access_token}, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message' : 'theater does not exist'})