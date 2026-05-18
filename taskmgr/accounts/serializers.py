from rest_framework import serializers
from .models import User
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ('id','username','email','password')
    def create(self, v):
        return User.objects.create_user(**v)
