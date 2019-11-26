from rest_framework import serializers
from lucky import models
from lucky.mixins import UserSerializer
from django.contrib.auth import authenticate, get_user_model, login
from lucky_day.utils import CustomApiException
from django.utils import timezone
import datetime


class signupserializer(serializers.ModelSerializer):

	class Meta:
		model = models.SignUp
		fields = ('first_name', 'last_name', 'mobile_number', 'password', 'country_code')

	def create(self, validated_data):
		a = models.SignUp.objects.get(mobile_number=validated_data.get('mobile_number'))
		if a:
			raise CustomApiException("mobile_number is already registered")
		user = get_user_model().objects.create_superuser(mobile_number=validated_data.get('mobile_number'), password=validated_data.get('password'), first_name=validated_data.get('first_name'), last_name=validated_data.get('last_name'), country_code=validated_data.get('country_code'))
		user.save()

		return user


class loginserializer(UserSerializer, serializers.ModelSerializer):

	class Meta:
		model = models.SignUp
		fields = (
            'mobile_number',
            'password'
            )

	def validate(self, data):
		user_auth = authenticate(mobile_number=data.get('mobile_number'), password=data.get('password'),)
		
		if not user_auth:
			raise CustomApiException("mobile_number or password is incorrect")
		
		self.user = user_auth
		user_auth.last_login = datetime.datetime.now(timezone.utc)
		user_auth.save()
		login(self.context['request'], user_auth)
		

		return data


class usermasterserializer(UserSerializer, serializers.ModelSerializer):

	class Meta:
		model = models.UserMaster
		fields = ('profile',)