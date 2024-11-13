from dataclasses import field
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
class EventTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event_Bookings
        fields='__all__'




class TurfBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=TurfBooking
        fields='__all__'
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

   
        



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        
        return token

class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            # Retrieve the user by email
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        # Check if the password matches
        if user.password != password:
            raise serializers.ValidationError("Invalid email or password.")
        
        attrs['user'] = user
        return attrs