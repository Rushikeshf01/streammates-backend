from django.contrib import admin
from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views
router = SimpleRouter()

router.register('rooms', views.RoomViewSet, basename='rooms')
router.register('room/participants', views.RoomParticipantsViewset, basename='room_participants')

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/a', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
