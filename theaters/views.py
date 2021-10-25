from django.http        import JsonResponse
from django.views       import View

from theaters.models    import *

class TheaterView(View):
    def get(self, request):
        cities = City.objects.all()
        ret    = [{'city':{'name': city.name, 'id': city.id}, 
                   'theater':[{'name': theater.name, 'id': theater.id} for theater in city.theater_set.all()]}
                    for city in cities]

        return JsonResponse(ret, safe=False, status=200)