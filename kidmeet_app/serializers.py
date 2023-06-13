from django.contrib.auth.models import User
from rest_framework import serializers

from kidmeet_app.models import Child


class CreateChildSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Child
        fields = ['id', 'name', 'age', 'interests', 'events', 'parent']


