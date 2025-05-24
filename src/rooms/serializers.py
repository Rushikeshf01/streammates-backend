from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Room, RoomParticipant
from .utils.room_code_generator import generate_room_code

User = get_user_model()


class RoomSerializers(serializers.ModelSerializer):

    room_code = serializers.SlugField(max_length=10, read_only=True)
    participants = serializers.StringRelatedField(many=True, read_only=True)
    host = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Room
        fields = ('room_name', 'room_code', 'host','is_active', 'participants')
    
    def create(self, validated_data):
        room_code = generate_room_code()
        print(validated_data)
        user = self.context['request'].user
        validated_data.update({"room_code": room_code, "host": user })
        room = Room.objects.create(**validated_data)
        return room

class RoomParticipantSerializer(serializers.ModelSerializer):

    room_code = serializers.SlugField(max_length=50, write_only=True)
    participant = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RoomParticipant
        fields = ('participant', 'room_code')

    def create(self, validated_data):
        code = validated_data.get('room_code', None)
        room_code = get_object_or_404(Room, room_code=code)
        # validated_data.update({"room_code": code})
        user = self.context['request'].user

        try:
            room_participants, created = RoomParticipant.objects.get_or_create(participant=user, room=room_code)
            # if not created:
            #     raise ValidationError({'detail': 'You have already joined this room.'})
            # else:
            #     room_participants = RoomParticipant.objects.create(participant=user, room=room_code)
            return room_participants
        except IntegrityError as e:
            raise ValidationError({'detail': 'A database error occurred.'})