from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    email = serializers.EmailField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, allow_null=False, allow_blank=False)
    first_name = serializers.CharField(write_only=True, required=True, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(write_only=True, required=True, allow_blank=False, allow_null=False)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        depth = 1
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        user = User(
            email=self.validated_data["email"],
            username=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"]
        )
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user




