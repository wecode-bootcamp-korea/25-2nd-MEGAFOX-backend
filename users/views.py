import jwt, requests, datetime

from django.http      import JsonResponse
from django.views     import View
from bookings.models import Booking
from megafox.utils import login_decorator

from users.models     import User
from megafox.settings import SECRET_KEY, ALGORITHM

class KakaoSignInView(View):
    def get(self, request):
        try:
            access_token = request.headers['Authorization']
            response     = requests.get('https://kapi.kakao.com/v2/user/me', headers=({'Authorization': f'Bearer {access_token}'})).json()

            if response.get('code') == -401:
                return JsonResponse({'message': 'INVALID_REQUEST'}, status=400)

            email        = response['kakao_account']['email']
            name         = response['kakao_account']['profile']['nickname']
            kakao_id     = response['id']

            user, created = User.objects.get_or_create(
                kakao_id = kakao_id,
                defaults = {
                    'name'  : name, 
                    'email' : email
                })

            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'message': access_token}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

class UserInfoView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        bookings = Booking.objects.select_related('movie_theater', 'user')\
                                  .filter(user_id=user.id, movie_theater__screen_time__gte=datetime.datetime.today())

        result = {
            "user_id" : user.id,
            "point" : user.point,
            "name" : user.name,
            "booking" : [{
                "count" : len(bookings), 
                "detail" : {
                    "booking_id" : booking.id
                }
            } for booking in bookings]
        }

        return JsonResponse({'result' : result}, status=200)
