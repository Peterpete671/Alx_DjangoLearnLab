from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Usefrom django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # explicit CharField as requested
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # use create_user() from get_user_model()
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        # create an auth token for the new user
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']
r
from django.contrib.auth import get_user_model

User = get_user_model

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

	def create(self, validated_data):
		user = User(
			username  = validated_data['username'],
			email = validated_data['email']
		)

		user.set_password(validated_data['password'])
		user.save()

		Token.objects.create(user=user)

		return user
