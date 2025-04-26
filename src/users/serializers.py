from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializers(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            'user':{
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email
            }
        })

        return data
class UserSerializers(serializers.ModelSerializer):
    
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('password not matched')
        return attrs

    def create(self, validated_data):
        user = User.objects.create( 
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', ''),
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password')

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        
        if password:
            instance.set_password(password)
        instance.save()
        return instance