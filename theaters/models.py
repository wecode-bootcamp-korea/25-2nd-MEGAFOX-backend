from django.db     import models

from core.models   import TimeStamp
from movies.models import Movie

class City(TimeStamp) :
  name = models.CharField(max_length=45)

  class Meta:
    db_table = 'cities'

class Theater(TimeStamp) :
  city = models.ForeignKey(City, on_delete=models.PROTECT)
  name = models.CharField(max_length=45)

  class Meta:
    db_table = 'theaters'

class MovieTheater(TimeStamp) :
  movie       = models.ForeignKey(Movie, on_delete=models.CASCADE)
  theater     = models.ForeignKey(Theater, on_delete=models.CASCADE)
  screen_time = models.DateTimeField()

  class Meta:
    db_table = 'movie_theaters'