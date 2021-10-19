from django.db     import models

from core.models   import TimeStamp
from users.models  import User
from movies.models import Movie

class ViewingPoint(TimeStamp) :
  name = models.CharField(max_length=45)
  
  class Meta:
    db_table = 'viewing_points'

class Review(TimeStamp) :
  user          = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  movie         = models.ForeignKey(Movie, on_delete=models.PROTECT)
  rating        = models.IntegerField()
  body          = models.CharField(max_length=200)

  class Meta:
    db_table = 'reviews'

class ReviewViewingPoint(TimeStamp) :
  review        = models.ForeignKey(Review, on_delete=models.PROTECT)
  viewing_point = models.ForeignKey(ViewingPoint, on_delete=models.PROTECT)

  class Meta:
    db_table = 'reviews_viewing_points'