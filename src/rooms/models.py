from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=100)
    room_code = models.SlugField(max_length=50, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hosted_room")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    password_protected = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.room_name

class RoomParticipant(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="participants")
    joined_at = models.DateTimeField(auto_now_add=True)
    is_host = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "participant"], name="unique_room_participant"
            )
        ]
    
    def __str__(self):
        return self.participant.username