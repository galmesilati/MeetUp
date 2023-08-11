from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from kidmeet_app.models import UserDetails, Address
from kidmeet_app.serializers.auth import UserSerializer


class ParentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'

    def save(self, **kwargs):
        address = Address(
            city=self.validated_data['city'],
            street=self.validated_data['street'],
            house_number=self.validated_data['house_number'],
            floor_number=self.validated_data.get('floor_number', None),
        )

        address.save()
        return address


class UserDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()

    def to_representation(self, instance):
        user_repr = super().to_representation(instance)
        user_data = user_repr['user']
        address_data = user_repr['address']
        user_details_data = {
            'phone_number': instance.phone_number,
            'birth_year': instance.birth_year
        }
        user_data.update(address_data)
        user_data.update(user_details_data)
        return user_data

    class Meta:
        model = UserDetails
        fields = ['phone_number', 'birth_year', 'user', 'address']

    def create(self, validated_data):
        with transaction.atomic():
            address = validated_data.pop('address')
            address_obj = Address.objects.create(**address)
            user = validated_data.pop('user')
            user_obj = User.objects.create_user(user['email'], email=user['email'], password=user['password'],
                                                first_name=user['first_name'],
                                                last_name=user['last_name'])
            details_obj = UserDetails.objects.create(user=user_obj, address=address_obj, **validated_data)
            return details_obj

