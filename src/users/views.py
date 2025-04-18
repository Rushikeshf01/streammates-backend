from django.contrib.auth import get_user_model
from django.conf import settings
from django.middleware import csrf
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializers

User = get_user_model()

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        access = response.data['access']
        refresh = response.data['refresh']

        response.set_cookie(
            key = settings.SIMPLE_JWT["AUTH_COOKIE_ACCESS"],
            value = access, 
            httponly = settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite = settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            expires = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure = settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            path = settings.SIMPLE_JWT["AUTH_COOKIE_PATH"] 
        )
        response.set_cookie(
            key = settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            value = refresh, 
            httponly = settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite = settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            expires = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure = settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            path = settings.SIMPLE_JWT["AUTH_COOKIE_PATH"] 
        )
        response.set_cookie(
                key='csrftoken',
                value=csrf.get_token(request)
        )
        # response.set_cookie('access_token', access, httponly=False, samesite='Lax', secure=False)
        # response.set_cookie('refresh_token', refresh, httponly=True, samesite='Lax', secure=False)
        # print("----------",response.cookies)

        return response

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers