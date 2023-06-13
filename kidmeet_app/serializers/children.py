from rest_framework import serializers

from kidmeet_app.models import Child


class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        exclude = ['user']
