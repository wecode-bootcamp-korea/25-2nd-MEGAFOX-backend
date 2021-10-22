import json
import datetime

from django.views          import View
from django.http           import JsonResponse
from django.db.models      import Count
from django.db             import transaction

from megafox.utils         import login_decorator
from bookings.models       import Booking
from movies.models         import Movie
from reviews.models        import Review, ViewingPoint , ReviewViewingPoint

class ReviewView(View):
    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            movie_id = int(request.GET.get('movieNo'))
            data     = json.loads(request.body)
            user     = request.user
            booking  = Booking.objects.select_related('movie_theater')\
                                      .get(user_id=user.id, movie_theater__movie_id=movie_id)

            if not 1 <= int(data['rating']) <= 10:
                return JsonResponse({'message' : 'INVALID_VALUE'}, status=400)
            
            if Review.objects.filter(user_id=user.id, movie_id=movie_id).exists():
                return JsonResponse({'message' : 'ALREADY_EXIST'}, status=400)

            review = Review.objects.create(
                user_id  = user.id,
                movie_id = movie_id,
                rating   = int(data['rating']),
                body     = data['body']
            )

            ReviewViewingPoint.objects.bulk_create(
                ReviewViewingPoint(
                    review_id        = review.id,
                    viewing_point_id = viewing_point
                ) for viewing_point in data['viewing_points']
            )

            time_diff = review.created_at - booking.movie_theater.screen_time
                                                        
            if time_diff <= datetime.timedelta(days=7):
                user.point += 50
                user.save()
            
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except Booking.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    
    def get(self, request):
        SORT_PREFIX = {
                'recent' : '-created_at',
                'rating' : '-rating',
                'like'   : '-like_count'
        } 
    
        try:
            offset        = int(request.GET.get('offset'))
            limit         = int(request.GET.get('limit'))
            order_request = request.GET.get('sort', 'recent')

            movie   = Movie.objects.get(id=request.GET.get('movieNo'))
            reviews = Review.objects.prefetch_related('reviewviewingpoint_set', 'userlikereview_set')\
                                    .select_related('user')\
                                    .filter(movie_id = movie.id)\
                                    .annotate(like_count=Count('userlikereview__review_id'))\
                                    .order_by(SORT_PREFIX[order_request])[offset:offset+limit]

            results = [{
                'review_id'      : review.id,
                'user_id'        : (review.user.email).split('@')[0][:-2] + '**',
                'rating'         : review.rating,
                'viewing_points' : [{
                    "id"   : point.viewing_point.id,
                    "name" : point.viewing_point.name
                } for point in review.reviewviewingpoint_set.all()],
                'body'           : review.body,
                'like_count'     : review.like_count
            } for review in reviews]

            return JsonResponse({'count' : len(results), 'results' : results}, status=200)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
        
        except Movie.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, review_id):
        try:
            user    = request.user
            review  = Review.objects.get(user_id=request.user.id, id=review_id)
            booking = Booking.objects.select_related('movie_theater')\
                                     .get(user_id=user.id, movie_theater__movie_id=review.movie_id)

            time_diff = review.created_at - booking.movie_theater.screen_time
                                                        
            if time_diff <= datetime.timedelta(days=7):
                user.point -= 50
                user.save()

            ReviewViewingPoint.objects.filter(review_id=review_id).delete()
            review.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        
        except Review.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
        


    @login_decorator
    @transaction.atomic
    def patch(self, request, review_id):      
        try:
            data   = json.loads(request.body)
            review = Review.objects.get(user_id=request.user.id, id=review_id)

            review.rating = data.get('rating', review.rating)
            review.body   = data.get('body', review.body)
            review.save()
            
            if data.get('viewing_points') :
                ReviewViewingPoint.objects.filter(review_id=review_id).delete()
                ReviewViewingPoint.objects.bulk_create(
                    ReviewViewingPoint(
                        review_id        = review.id,
                        viewing_point_id = viewing_point
                    ) for viewing_point in data['viewing_points']
                )
            
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except Review.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
