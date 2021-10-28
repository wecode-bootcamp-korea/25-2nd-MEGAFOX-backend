import datetime

from django.http        import JsonResponse
from django.views       import View

from movies.models      import *
from reviews.models     import *
from likes.models       import *
from theaters.models    import *
from django.db.models   import Avg, Q

class MovieListView(View):
        
    def get(self, request):
        sort         = request.GET.get('sort', None)
        offset       = int(request.GET.get('offset', 0))
        limit        = int(request.GET.get('limit', 20))
        movie_search = request.GET.get('search', None)
        q            = Q()

        if sort == 'released':
            q.add(Q(release_date__lte=datetime.date(2021, 10, 10)), q.AND)
        if movie_search :
            q.add(Q(ko_name__contains=movie_search), q.AND)

        movie_list = Movie.objects.filter(q).order_by('-total_audience')[offset:limit+offset]
        ret = [{
            'movie_id'     : movie.id,
            'ko_name'      : movie.ko_name,
            'release_date' : movie.release_date,
            'age_rate'     : movie.age_rate,
            'like'         : UserLikeMovie.objects.filter(movie_id=movie.id).count(),
            'image'        : list(movie.image_set.values('main_image_url')),
            'description'  : movie.description,
            'avg_rating'   : Review.objects.filter(movie_id=movie.id).aggregate(rating_avg=Avg('rating')).get('rating_avg')
        } for movie in movie_list]
    
        return JsonResponse(ret, safe=False, status=200)

class MovieDetailView(View):
    def get(self, request, movie_id):
        try:
            movie   = Movie.objects.get(id=movie_id)
            reviews = Review.objects.filter(movie_id=movie_id)
            rating  = reviews.aggregate(rating_avg = Avg('rating'))['rating_avg']

            ret = [{
                'movie_id'       : movie.id,
                'ko_name'        : movie.ko_name,
                'eng_name'       : movie.eng_name,
                'avg_rating'     : rating,
                'total_audience' : movie.total_audience,
                'description'    : movie.description,
                'review'         : list(reviews.values('user', 'rating', 'body')),
                'screen_type'    : movie.screen_type,
                'director'       : movie.director,
                'genre'          : str(movie.genre) + '/' + str(movie.running_time) + '분',
                'age_rate'       : movie.age_rate,
                'release_date'   : movie.release_date,
                'actor'          : movie.actor,
                'like'           : UserLikeMovie.objects.filter(movie_id=movie.id).count(),
                'images'         : list(movie.image_set.values('main_image_url', 'sub_image_url'))
            }]

            return JsonResponse(ret, safe=False, status=200)
        
        except Movie.DoesNotExist:
            return JsonResponse({'message' : 'movie_does_not_exist'}, status=400)