from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from . models import PicDirectory
from . serializers import PicDirectorySerializer
from . serializers import ImageSerializer
from . import main_model
import os


# Create your views here.
def band(request, band_id):
    return render(request, 'band/band.html')


def all_band(request):
    return render(request, 'band/all_band.html')


class pictureList(APIView):

    def get(self, request):
        pictures = PicDirectory.objects.all()
        serializer = PicDirectorySerializer(pictures, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ImageSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            filename = serializer.data['image']
            filename = ".." + filename
            print filename

            # this is our main model
            disease = main_model.disease(filename)
            return Response({"disease": disease, "filename": serializer.data['image']}, status=201)

        return Response(serializer.errors, status=400)
