from django.test      import TestCase, Client

from movies.models  import *
from users.models   import *
from likes.models   import UserLikeMovie
from reviews.models import Review

class MovieListDetailTest(TestCase):
    def setUp(self):
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

        Image.objects.bulk_create([
            Image(movie_id = 1, main_image_url = 'naver.com', sub_image_url = 'naver.com'),
            Image(movie_id = 2, main_image_url = 'naver.com', sub_image_url = 'naver.com'),
            Image(movie_id = 3, main_image_url = 'naver.com', sub_image_url = 'naver.com')
        ])

        User.objects.create(
            id            = 1,
            email         = 'gmail@gmail.com',
            name          = 'wecode',
            point         = 100000,
            kakao_id      = 'dummy1234',
            date_of_birth = '2000-01-01',
            phone_number  = '01015771577'
        )

        Review.objects.bulk_create([
            Review(user_id = 1, movie_id = 1, rating = 9, body = 'good'),
            Review(user_id = 1, movie_id = 2, rating = 9, body = 'great'),
            Review(user_id = 1, movie_id = 3, rating = 9, body = 'perfect')
        ])

        UserLikeMovie.objects.bulk_create([
            UserLikeMovie(user_id = 1, movie_id = 1),
            UserLikeMovie(user_id = 1, movie_id = 2),
            UserLikeMovie(user_id = 1, movie_id = 3)
        ])

    def tearDown(self):
        Image.objects.all().delete()
        Review.objects.all().delete()
        UserLikeMovie.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()

    def test_movielist_get_success(self):
        client = Client()
        response = client.get('/movie', content_type='application/json')
        self.assertEqual(response.json(),
        [{
            'movie_id'     : 1,
            'ko_name'      : '베놈',
            'release_date' : '2021-10-10',
            'age_rate'     : '전체이용',
            'like'         : 1,
            'image'        : [{'main_image_url': 'naver.com'}],
            'description'  : 'aaaaaaaaaaaa',
            'avg_rating'   : 9
        }, {
            'movie_id'     : 2,
            'ko_name'      : '베놈2',
            'release_date' : '2021-10-12',
            'age_rate'     : '전체이용',
            'like'         : 1,
            'image'        : [{'main_image_url': 'naver.com'}],
            'description'  : 'cccccccc',
            'avg_rating'   : 9
        }, {
            'movie_id'     : 3,
            'ko_name'      : '베놈3',
            'release_date' : '2021-11-11',
            'age_rate'     : '전체이용',
            'like'         : 1,
            'image'        : [{'main_image_url': 'naver.com'}],
            'description'  : 'bbbbbbbb',
            'avg_rating'   : 9
        }])

        self.assertEqual(response.status_code, 200)

    def test_movielist_get_filter_by_release_day_success(self):
        client = Client()

        response = client.get('/movie?sort=released', content_type='application/json')
        self.assertEqual(response.json(),
           [{
               'movie_id'     : 1,
               'ko_name'      : '베놈',
               'release_date' : '2021-10-10',
               'age_rate'     : '전체이용',
               'like'         : 1,
               'image'        : [{'main_image_url': 'naver.com'}],
               'description'  : 'aaaaaaaaaaaa',
               'avg_rating'   : 9
        }])
        self.assertEqual(response.status_code, 200)

    def test_movielist_get_search_movie_success(self):
        client = Client()

        response = client.get('/movie?search=베놈2', content_type='application/json')
        self.assertEqual(response.json(),
           [{
               'movie_id'     : 2,
               'ko_name'      : '베놈2',
               'release_date' : '2021-10-12',
               'age_rate'     : '전체이용',
               'like'         : 1,
               'image'        : [{'main_image_url': 'naver.com'}],
               'description'  : 'cccccccc',
               'avg_rating'   : 9
        }])
        self.assertEqual(response.status_code, 200)
        
    def test_moviedetail_get_success(self):
        client = Client()

        response = client.get('/movie/1', content_type='application/json')
        self.assertEqual(response.json(),
        [{
            'movie_id'       : 1,
            'ko_name'        : '베놈',
            'eng_name'       : 'venom',
            'avg_rating'     : 9,
            'total_audience' : 123456,
            'description'    : 'aaaaaaaaaaaa',
            'review'         : [{'user': 1, 'rating': 9, 'body': 'good'}],
            'screen_type'    : '1',
            'director'       : 'wecode',
            'genre'          : '코미디'+'/'+'120'+'분',
            'age_rate'       : '전체이용',
            'release_date'   : '2021-10-10',
            'actor'          : '김김김, 박박박',
            'like'           : 1,
            'images'         : [{'main_image_url': 'naver.com', 'sub_image_url': 'naver.com'}]
        }])

        self.assertEqual(response.status_code, 200)

    def test_moviedetail_get_doesnotexist(self):
        client = Client()

        response = client.get('/movie/5', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'movie_does_not_exist'
            })