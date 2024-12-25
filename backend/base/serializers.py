from rest_framework import serializers
from .models import Note

class NoteSearilizer(serializers.ModelSerializer):
    
    class Meta:
        model=Note
        fields=['id','description']