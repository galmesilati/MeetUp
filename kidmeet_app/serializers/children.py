from django.db import transaction
from rest_framework import serializers

from kidmeet_app.models import Child, Event, Interests, ChildInterests, Schedule


# class CreateChildSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Child
#         fields = ['child_name', 'age']


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        # exclude = ['user_id']
        fields = '__all__'


class AvailableChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['child_id', 'name', 'age', 'interests']


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


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

# class UserDetailsSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     address = AddressSerializer()
#
#     class Meta:
#         model = UserDetails
#         fields = ['phone_number', 'birth_year', 'user', 'address']
#
#     def create(self, validated_data):
#         address = validated_data.pop('address')
#         address_obj = Address.objects.create(**address)
#         user = validated_data.pop('user')
#         user_obj = User.objects.create_user(user['email'], email=user['email'], password=user['password'],
#                                             first_name=user['first_name'],
#                                             last_name=user['last_name'])
#         details_obj= UserDetails.objects.create(user=user_obj, address=address_obj, **validated_data)
#         return details_obj


# class CreateChildSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Child
#         fields = ['child_name', 'age']
