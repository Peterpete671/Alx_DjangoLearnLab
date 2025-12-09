from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User

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
