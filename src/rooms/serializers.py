from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

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
        room = get_object_or_404(Room, room_code=code)
        # validated_data.update({"room_code": code})
        user = self.context['request'].user
        room_participants = RoomParticipant.objects.create(participant=user, room=room)
        return room_participants