from rest_framework import serializers
from .models import Gallery


#Gallery Serializer
class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = '__all__'
