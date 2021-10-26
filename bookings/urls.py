from django.urls import path

from bookings.views import BookingView, ReserveView
urlpatterns = [
    path('', BookingView.as_view()),
    path('/reserve', ReserveView.as_view())
]
