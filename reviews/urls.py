from django.urls import path

from reviews.views import *

urlpatterns = [
    path('/comment', ReviewView.as_view()),
    path('/comment/<int:review_id>', ReviewView.as_view())
]
