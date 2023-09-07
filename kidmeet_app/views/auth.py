import uuid

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from kidmeet_app.models import Address
from kidmeet_app.models import UserDetails
from kidmeet_app.serializers.auth import UserSerializer
from kidmeet_app.serializers.users_parents import UserDetailsSerializer, AddressSerializer

from google.oauth2 import id_token
from google.auth.transport import requests


@api_view(['POST'])
def signup(request):
    print('signup')
    new_user_serializer = UserDetailsSerializer(data=request.data)
    new_user_serializer.is_valid(raise_exception=True)
    new_user_serializer.save()
    return Response(new_user_serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def me(request):
    # you will get here only if the user is already authenticated!
    user_serializer = UserSerializer(instance=request.user, many=False)
    print(request.user)
    return Response(data=user_serializer.data)


@api_view(['POST'])
def google_login(request):
    google_jwt = request.data['google_jwt']
    CLIENT_ID = '53237428834-qsadkjv4872evoit81fpg1g5h7bufbih.apps.googleusercontent.com'
    try:
        idinfo = id_token.verify_oauth2_token(google_jwt, requests.Request(), CLIENT_ID)
        email = idinfo['email']
        try:
            user = User.objects.get(email=email)
            print('user found')
            print(user)
            # creating jwt manually

        except User.DoesNotExist:
            print('does not exist')
            user = User.objects.create_user(username=email, email=email, password=str(uuid.uuid4()),
                                     first_name=idinfo['given_name'], last_name=idinfo['family_name'])

        refresh = RefreshToken.for_user(user)
        return Response(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

        print(idinfo)
    except ValueError as e:
        print(e)
    print(google_jwt)
    return Response()

