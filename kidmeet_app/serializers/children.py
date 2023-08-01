from django.db import transaction
from rest_framework import serializers

from kidmeet_app.models import Child, Event, Interests, ChildInterests, Schedule, ChildEvent


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class AvailableChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['child_id', 'name', 'age', 'interests']


class EventSerializer(serializers.ModelSerializer):
    child_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        child_id = validated_data.pop('child_id')
        event = Event.objects.create(**validated_data)

        if child_id:
            with transaction.atomic():
                child = Child.objects.get(pk=child_id)
                ChildEvent.objects.create(child=child, event=event)

            return event

        # def update(self, instance, validated_data):
        #     previous_event_id = instance.event.event_id
        #     new_event_id = validated_data['event'].id



class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = '__all__'


class ChildInterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildInterests
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'







