from django.contrib.auth.models import User
from rest_framework import serializers

from kidmeet_app.models import UserDetails, Address


class ParentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

    def save(self, address, **kwargs):
        print('address:', address, 'kwargs:', kwargs)
        new_user_details = UserDetails(
            user=self.instance,
            phone_number=self.validated_data['phone_number'],
            birth_year=self.validated_data['birth_year'],
            address=address
        )
        new_user_details.save()

        return new_user_details


class AdressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


    def save(self, **kwargs):
        address = Address(
            city=self.validated_data['city'],
            street=self.validated_data['street'],
            house_number=self.validated_data['house_number'],
            floor_number=self.validated_data['floor_number'],
        )

        address.save()
        return address
