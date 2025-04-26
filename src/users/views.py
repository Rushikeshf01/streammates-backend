from django.contrib.auth import get_user_model
from django.conf import settings
from django.middleware import csrf
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializers, CustomTokenObtainPairSerializers

User = get_user_model()

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        access = response.data.pop('access', None)
        refresh = response.data.pop('refresh', None)

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
                value=csrf.get_token(request),
                httponly = settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                # samesite = settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                # expires = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                # secure = settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                # path = settings.SIMPLE_JWT["AUTH_COOKIE_PATH"]
        )

        print('-------------',response.cookies)
        # response.set_cookie('access_token', access, httponly=False, samesite='Lax', secure=False)
        # response.set_cookie('refresh_token', refresh, httponly=True, samesite='Lax', secure=False)
        # print("----------",response.cookies)

        # return Response({'LoggedIn': 'True'})
        return response
    
    serializer_class = CustomTokenObtainPairSerializers

class VerifyLoginView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        return Response({'user':{
            'id': user.id,
            'username': user.username,
            'email': user.email
        }})

class Logoutview(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)

            # token.blacklist()
        except Exception:
            return Response({"message": "logout failed"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response({"message": "logout successfully"}, status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers