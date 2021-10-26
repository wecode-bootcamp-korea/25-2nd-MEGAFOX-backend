from django.urls import path

from .views import *

urlpatterns = [
    path('/movie/<int:movie_id>', UserLikeMovieView.as_view()),
    path('/review/<int:review_id>', UserLikeReviewView.as_view()),
    path('/theater/<int:theater_id>', UserLikeTheaterView.as_view())
]