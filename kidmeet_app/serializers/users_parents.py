from django.contrib.auth.models import User
from rest_framework import serializers


class ParentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
