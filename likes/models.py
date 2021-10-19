from django.db      import models

from core.models    import TimeStamp
from users.models   import User
from movies.models  import Movie, Theater
from reviews.models import Review

class UserLikeMovie(TimeStamp):
  user  = models.ForeignKey(User, on_delete=models.CASCADE)
  movie = models.ForeignKey(Movie, on_delete=models.PROTECT)

  class Meta:
    db_table = 'user_like_movies'
  
class UserLikeReview(TimeStamp):
  user   = models.ForeignKey(User, on_delete=models.CASCADE)
  review = models.ForeignKey(Review, on_delete=models.CASCADE)

  class Meta:
    db_table = 'user_like_reviews'

class UserLikeTheater(TimeStamp):
  user    = models.ForeignKey(User, on_delete=models.CASCADE)
  theater = models.ForeignKey(Theater, on_delete=models.CASCADE)

  class Meta:
    db_table = 'user_like_theaters'