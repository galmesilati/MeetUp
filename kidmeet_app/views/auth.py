from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from kidmeet_app.models import Address
from kidmeet_app.models import UserDetails
from kidmeet_app.serializers.auth import UserSerializer
from kidmeet_app.serializers.users_parents import UserDetailsSerializer, AddressSerializer


@api_view(['POST'])
def signup(request):
    new_user = UserSerializer(data=request.data)
    if new_user.is_valid():
        new_user.save()
        user = User.objects.get(email=new_user.data['email'])
        print('user:', user)
        if request.data.get('floor_number') is None:
            request.data["floor_number"] = 0
        new_address = AddressSerializer(data=request.data)
        if new_address.is_valid():
            new_address.save()
            address = Address.objects.get(city=new_address.data['city'],
                                          street=new_address.data['street'],
                                          house_number=new_address.data['house_number'],
                                          floor_number=new_address.data['floor_number'])
            print('address', address, 'user', user)
            user_details = UserDetailsSerializer(data=request.data)
            if user_details.is_valid():
                user_details.save(user=user, address=address)
                print('user details:', user_details)
            else:
                print('user details:', user_details.errors)
            return Response(data=new_user.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_address.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def me(request):
    # you will get here only if the user is already authenticated!
    user_serializer = UserSerializer(instance=request.user, many=False)
    return Response(data=user_serializer.data)
