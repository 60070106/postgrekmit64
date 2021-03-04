from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserImage
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import datetime

import base64
from PIL import Image
from io import BytesIO


User = get_user_model()

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserImage
        fields = ['imgpath',]

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=12)
    image = ImageSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'image']

class RegisterSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'first_name', 'last_name', 'image']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})

    #     return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['last_name'],
        )

        userimage = UserImage.objects.create(user=user, imgpath=validated_data['image'][0]['imgpath'])

        user.set_password(validated_data['password'])


        data = validated_data['image'][0]['imgpath']
        im = Image.open(BytesIO(base64.b64decode(data)))
        im.save(validated_data['username']+'.png', 'PNG')

        userimage.save()
        user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializer(self.user)

        user = User.objects.get(username=self.user.username)
        user.last_login = datetime.datetime.now()
        user.save()

        return { 
            "success" : True,
            "token" : data["access"],
            "user" : serializer.data,
        }