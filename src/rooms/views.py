from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Room, RoomParticipant
from .serializers import RoomSerializers, RoomParticipantSerializer

# Create your views here.
class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers
    permission_classes = [IsAuthenticated]

class RoomParticipantsViewset(ModelViewSet):
    queryset = RoomParticipant.objects.all()
    serializer_class = RoomParticipantSerializer
    permission_classes = [IsAuthenticated]