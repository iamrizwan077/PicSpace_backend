from dataclasses import fields
from rest_framework import serializers
from .models import CustomUser, Gallery
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GallerySerializer(serializers.ModelSerializer):
#  name=serializers.CharField()
 # image=serializers.ImageField()
  #date=serializers.DateTimeField()
  
  class Meta:
    model=Gallery
    fields = '__all__' 

class CustomUserSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True)
  username=serializers.CharField()
  password = serializers.CharField(min_length=8, write_only=True)

  class Meta:
    model = CustomUser
    fields = ('email','username','password')
    extra_kwargs = {'password': {'write_only':True}}
  
  def create(self, validated_data):
    password = validated_data.pop('password', None)
    instance = self.Meta.model(**validated_data)
    if password is not None:
      instance.set_password(password)
    instance.save()
    return instance
    