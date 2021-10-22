from django.db       import models

from core.models     import TimeStamp
from users.models    import User
from theaters.models import MovieTheater

class Booking(TimeStamp) :
  user          = models.ForeignKey(User, on_delete=models.CASCADE)
  movie_theater = models.ForeignKey(MovieTheater, on_delete=models.PROTECT)
  total_price   = models.DecimalField(max_digits=15, decimal_places=3)
  adult         = models.IntegerField(null=True)
  teenager      = models.IntegerField(null=True)
  kid           = models.IntegerField(null=True)

  class Meta:
    db_table = 'bookings'