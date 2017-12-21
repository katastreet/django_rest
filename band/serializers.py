
from rest_framework import serializers
from .models import PicDirectory
from drf_extra_fields.fields import Base64ImageField


class PicDirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PicDirectory
        fields = ('filename',)


class ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = PicDirectory
        fields = ('filename', 'image')

    def create(self, validated_data):
        image = validated_data.pop('image')
        filename = validated_data.pop('filename')
        return PicDirectory.objects.create(filename=filename, image=image)
