from django.db import transaction
from rest_framework import serializers

from kidmeet_app.models import Child, Event, Interests, ChildInterests, Schedule, ChildEvent


class ChildSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(many=True, queryset=Interests.objects.all())

    class Meta:
        model = Child
        # fields = ['user', 'name', 'age', 'interests']
        fields = '__all__'

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        print(validated_data)
        return super().create(validated_data)
        # return super(ChildSerializer, self).create(validated_data)


class AvailableChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['child_id', 'name', 'age', 'interests']


class EventSerializer(serializers.ModelSerializer):
    # child_id = serializers.IntegerField(write_only=True, required=False)
    children = serializers.PrimaryKeyRelatedField(many=True, queryset=Child.objects.all(),required=False)

    class Meta:
        model = Event
        fields = ['event_id', 'title', 'description', 'start_event', 'end_event', 'location', 'children']

    def create(self, validated_data):
        # child_id = validated_data.pop('child_id')
        children_data = validated_data.pop('children', [])
        event = Event.objects.create(**validated_data)

        for child in children_data:
            # child = Child.objects.get(pk=child['child_id'])
            ChildEvent.objects.create(child=child, event=event)

        # if child_id:
        #     with transaction.atomic():
        #         child = Child.objects.get(pk=child_id)
        #         ChildEvent.objects.create(child=child, event=event)

            return event


class InterestsSerializer(serializers.ModelSerializer):
    child_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Interests
        fields = '__all__'

    def create(self, validated_data):
        child_id = validated_data.pop('child_id')
        interest = Interests.objects.create(**validated_data)

        if child_id:
            with transaction.atomic():
                child = Child.objects.get(pk=child_id)
                ChildInterests.objects.create(child=child, interest=interest)

        return interest


class ChildInterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildInterests
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'







