from django.urls import path

from users.views import KakaoSignInView, UserInfoView

urlpatterns = [
  path('/kakao/signin', KakaoSignInView.as_view()),
  path('/info', UserInfoView.as_view())
]
