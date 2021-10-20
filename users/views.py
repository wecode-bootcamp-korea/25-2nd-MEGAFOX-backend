import jwt, requests

from django.http      import JsonResponse
from django.views     import View

from users.models     import User
from megafox.settings import SECRET_KEY, ALGORITHM

class KakaoSignInView(View):
    def get(self, request):
        try:
            access_token = request.headers['Authorization']
            response     = requests.get('https://kapi.kakao.com/v2/user/me', headers=({'Authorization': f'Bearer {access_token}'})).json()
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

            return JsonResponse({'access_token' : access_token}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)