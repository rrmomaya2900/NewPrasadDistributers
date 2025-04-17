# app_name/serializers.py
from rest_framework import serializers
from .models import GSTDeclaration

class GSTDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSTDeclaration
        fields = '__all__'  # Include all fields
        
