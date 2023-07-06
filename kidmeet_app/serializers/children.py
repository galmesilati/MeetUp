from rest_framework import serializers

from kidmeet_app.models import Child, Event, Interests, ChildInterests


class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        # exclude = ['user_id']
        fields = '__all__'


class DetailedEventChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class InterestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interests
        fields = '__all__'


class ChildInterestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChildInterests
        fields = '__all__'




