from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()

router.register('rooms', views.RoomViewSet, basename='rooms')
router.register('room/participants', views.RoomParticipantsViewset, basename='room_participants')

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
