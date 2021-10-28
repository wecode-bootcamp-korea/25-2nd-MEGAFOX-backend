from django.test     import TestCase, Client

from movies.models   import *
from theaters.models import *

class TheaterTest(TestCase):
    def setUp(self):
        City.objects.bulk_create([
            City(id = 1, name = '서울'),
            City(id = 2, name = '대구')
        ])

        Theater.objects.bulk_create([
            Theater(id = 1, city_id = 1, name = '신촌'),
            Theater(id = 2, city_id = 1, name = '압구정'),
            Theater(id = 3, city_id = 2, name = '동대구'),
            Theater(id = 4, city_id = 2, name = '대구')
        ])
    def tearDown(self):
        Theater.objects.all().delete()
        City.objects.all().delete()
    
    def test_theater_get_success(self):
        client = Client()

        response = client.get('/theaters', content_type='application/json')
        self.assertEqual(response.json(),
        [{
            'city': {
                'name': '서울',
                'id'  : 1    
            },
            'theater' : [{
                    'name': '신촌',
                    'id'  : 1
                },{
                    'name': '압구정',
                    'id'  : 2
                }]
        },{
            'city': {
                'name': '대구',
                'id'  : 2    
            },
            'theater' : [{
                    'name': '동대구',
                    'id'  : 3
                },{
                    'name': '대구',
                    'id'  : 4
                }]
        }])

        self.assertEqual(response.status_code, 200)