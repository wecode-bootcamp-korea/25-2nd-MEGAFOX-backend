from django.http        import JsonResponse
from django.views       import View

from megafox.utils      import login_decorator
from likes.models       import *
from movies.models      import *
from theaters.models    import *
from reviews.models     import *

class UserLikeMovieView(View):
    @login_decorator
    def post(self, request, movie_id):
        try:
            user          = request.user
            movie         = Movie.objects.get(id=movie_id)
            like, created = UserLikeMovie.objects.get_or_create(user=user, movie=movie)

            if not created:
                like.delete()
                return JsonResponse({'message' : 'deleted'}, status=200)

            return JsonResponse({'message' : 'success'}, status=201)
        
        except Movie.DoesNotExist:
            return JsonResponse({'message' : 'movie does not exist'}, status=404)
    
class UserLikeReviewView(View):
    @login_decorator
    def post(self, request, review_id):
        try:
            user          = request.user
            review        = Review.objects.get(id=review_id)
            like, created = UserLikeReview.objects.get_or_create(user=user, review=review)

            if not created:
                like.delete()
                return JsonResponse({'message' : 'deleted'}, status=200)

            return JsonResponse({'message' : 'success'}, status=201)
        
        except Review.DoesNotExist:
            return JsonResponse({'message' : 'review does not exist'}, status=404)

class UserLikeTheaterView(View):
    @login_decorator
    def post(self, request, theater_id):
        try:
            user          = request.user
            theater       = Theater.objects.get(id=theater_id)
            like, created = UserLikeTheater.objects.get_or_create(user=user, theater=theater)

            if not created:
                like.delete()
                return JsonResponse({'message' : 'deleted'}, status=200)

            return JsonResponse({'message' : 'success'}, status=201)
        
        except Theater.DoesNotExist:
            return JsonResponse({'message' : 'theater does not exist'}, status=404)