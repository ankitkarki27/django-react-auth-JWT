from django.shortcuts import render
from django.contrib.auth.models import User
from.models import Note
from.serializers import NoteSearilizer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes(request):
    user = request.user
    notes=Note.objects.filter(owner=user)
    serializer=NoteSearilizer(notes,many=True)
    return Response(serializer.data)



# Create your views here.
