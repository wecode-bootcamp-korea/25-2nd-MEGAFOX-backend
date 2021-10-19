from django.db   import models

from core.models import TimeStamp

class User(TimeStamp) :
  email         = models.CharField(max_length=100, unique=True, null=True)
  name          = models.CharField(max_length=45)
  point         = models.IntegerField(default=0)
  kakao_id      = models.CharField(max_length=200)
  date_of_birth = models.DateField(null=True)
  phone_number  = models.CharField(max_length=100, null=True)

  class Meta:
    db_table = 'users'