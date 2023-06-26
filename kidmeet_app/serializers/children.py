from rest_framework import serializers

from kidmeet_app.models import Child, Event


class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        exclude = ['user_id']


class DetailedEventChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'child': {
                'required': False,
                'validators': None,
            }
        }


