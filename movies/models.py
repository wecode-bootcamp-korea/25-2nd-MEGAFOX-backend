from django.db    import models

from core.models  import TimeStamp

class City(TimeStamp) :
  name = models.CharField(max_length=45)

  class Meta:
    db_table = 'cities'

class Theater(TimeStamp) :
  city = models.ForeignKey(City, on_delete=models.PROTECT)
  name = models.CharField(max_length=45)

  class Meta:
    db_table = 'theaters'

class Movie(TimeStamp) :
  ko_name        = models.CharField(max_length=45)
  eng_name       = models.CharField(max_length=45)
  release_date   = models.DateField()
  close_date     = models.DateField()
  screen_type    = models.CharField(max_length=45)
  director       = models.CharField(max_length=45)
  genre          = models.CharField(max_length=45)
  running_time   = models.IntegerField()
  age_rate       = models.CharField(max_length=45)
  actor          = models.CharField(max_length=200)
  total_audience = models.IntegerField()
  description    = models.TextField()

  class Meta :
    db_table = 'movies'

class MovieTheater(TimeStamp) :
  movie       = models.ForeignKey(Movie, on_delete=models.CASCADE)
  theater     = models.ForeignKey(Theater, on_delete=models.CASCADE)
  screen_time = models.DateTimeField()

  class Meta:
    db_table = 'movie_theaters'

class Image(TimeStamp) :
  movie          = models.ForeignKey(Movie, on_delete=models.PROTECT)
  main_image_url = models.CharField(max_length=1000)
  sub_image_url  = models.CharField(max_length=1000)

  class Meta:
    db_table = 'images'

  
