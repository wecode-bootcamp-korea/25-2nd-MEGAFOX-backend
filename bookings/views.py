import json
import datetime
import enum

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q 
from likes.models     import UserLikeTheater

from megafox.utils   import login_decorator
from bookings.models import Booking
from movies.models   import Image, Movie
from theaters.models import MovieTheater, City
from likes.models    import UserLikeTheater

TODAY = datetime.datetime.today().replace(tzinfo=datetime.timezone.utc)

class Price(enum.Enum):
    ADULT    = 10000 
    TEENAGER = 8000
    KID      = 6000

def calculate_total_price(adult, teenager, kid):
    return adult * Price.ADULT.value + teenager * Price.TEENAGER.value + kid * Price.KID.value

def calculate_end_time(screen_time, running_time):
    H, M = divmod(running_time, 60)
    return datetime.datetime.strftime(screen_time + datetime.timedelta(hours=H, minutes=M), "%H:%M")

class BookingView(View):
    @login_decorator
    def get(self, request):
        user     = request.user
        bookings = Booking.objects.select_related('movie_theater', 'user')\
                                  .filter(user_id = user.id, movie_theater__screen_time__gte=TODAY)
                                    
        results = [{
            "id"           : booking.id,
            "movie_image"  : Image.objects.get(movie_id=booking.movie_theater.movie.id).main_image_url,
            "theater"      : booking.movie_theater.theater.name,
            "movie_name"   : booking.movie_theater.movie.ko_name,
            "screen_time"  : format(booking.movie_theater.screen_time,"%Y.%m.%d %A %H:%M"),
            "people"       : {
                "adult"    : booking.adult,
                "teenager" : booking.teenager,
                "kid"      : booking.kid
            },
            "booking_date" : format(booking.created_at, "%Y.%m.%d")
        }for booking in bookings]

        return JsonResponse({'results' : results}, status=200)

class ReserveView(View):
    @login_decorator
    def post(self, request):
        try :
            user             = request.user
            data             = json.loads(request.body)
            movie_theater_id = data['movie_theater_id']
            adult            = int(data.get('adult'))
            teenager         = int(data.get('teenager'))
            kid              = int(data.get('kid'))

            if MovieTheater.objects.get(id=movie_theater_id).screen_time < TODAY:
                return JsonResponse({'message' : 'INVALID_ACCESS'}, status=400)

            if Booking.objects.filter(user_id=user.id, movie_theater_id=movie_theater_id).exists():
                return JsonResponse({'message' : 'ALREADY_EXIST'}, status=400)

            Booking.objects.create(
                user_id          = user.id,
                movie_theater_id = movie_theater_id,
                adult            = adult,
                teenager         = teenager,
                kid              = kid,
                total_price      = calculate_total_price(adult=adult, teenager=teenager, kid=kid)
            )

            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except MovieTheater.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

    @login_decorator
    def get(self, request):
        user_like_theaters = UserLikeTheater.objects.filter(user_id=request.user.id)

        date     = request.GET.get('date', datetime.datetime.strftime(TODAY, '%Y-%m-%d'))
        movie    = request.GET.get('movieNo', None)
        city     = request.GET.get('city', None)
        theaters = request.GET.getlist('theater_id', list(user_like_theaters.values_list('theater_id', flat=True)))

        q = Q()

        if date:
            q.add(Q(screen_time__day=datetime.datetime.strptime(date, '%Y-%m-%d').day), q.AND)
            q.add(Q(screen_time__month=datetime.datetime.strptime(date, '%Y-%m-%d').month), q.AND)
            q.add(Q(screen_time__year=datetime.datetime.strptime(date, '%Y-%m-%d').year), q.AND)
        
        if movie:
            q.add(Q(movie__id=movie),q.AND)
        
        if city:
            q.add(Q(theater__city_id=city), q.AND)

        if theaters:
            q.add(Q(theater_id__in=theaters), q.AND)

        movie_theater = MovieTheater.objects.filter(q).prefetch_related('movie', 'theater')

        if not movie_theater:
            return JsonResponse({'message' : 'MOVIE_OR_THEATER_DOES_NOT_EXIST'}, status=404)
        
        filtered_movies = [{
            "movie_id"           : movie.movie.id,
            "movie_name"         : movie.movie.ko_name,
            "movie_theater_id"   : movie.theater.id,
            "movie_theater_name" : movie.theater.name,
            "start_time"         : movie.screen_time.strftime('%H:%M'),
            "end_time"           : calculate_end_time(movie.screen_time, movie.movie.running_time),
        } for movie in movie_theater]

        theater_list = [{
            "city_id"        : city.id,
            "city_name"      : city.name,
            "theater_count"  : len(city.theater_set.all()),
            "theater" : [{
                "theater_id"   : theater.id,
                "theater_name" : theater.name
            } for theater in city.theater_set.all()]
        } for city in City.objects.prefetch_related('theater_set').all()]

        movie_list = [{
            "movie_id"     : movie.id,
            "movie_name"   : movie.ko_name,
            "age_rate"     : movie.age_rate,
            "is_userlike"  : movie.userlikemovie_set.filter(movie_id=movie.id, user_id=request.user.id).exists(),
            "is_available" : movie_theater.filter(movie__id=movie.id).exists(),
            "poster"       : Image.objects.get(movie_id=movie.id).main_image_url,
        } for movie in Movie.objects.prefetch_related('userlikemovie_set').all()]

        like_theaters = user_like_theaters.all()

        liked_theaters = [{
            "city_id" : 0,
            "city_name" : "선호극장",
            "theater_count" : len(like_theaters),
            "theater" : [{
                "theater_id"   : theater.id,
                "theater_name" : theater.theater.name
            } for theater in like_theaters]}]

        result = {
            "movie_list"     : movie_list,
            "theater_list"   : liked_theaters + theater_list, 
            "movie_info"     : filtered_movies,
        }

        return JsonResponse({"result" : result}, status=200)