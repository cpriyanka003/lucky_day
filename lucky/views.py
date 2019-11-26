from rest_framework import generics, viewsets
from rest_framework.response import Response
from lucky import models, serializers
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
import jwt, json
from lucky_day import settings
from django.contrib import auth


class signup(generics.CreateAPIView):
	serializer_class = serializers.signupserializer
	model = models.SignUp

	def create(self, request, *args, **kwargs):
		try:
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			self.perform_create(serializer)
			return Response({'message': 'Data Added successfully', 'success': True})
		except Exception as e:
			return Response({'message': format(e.args[-1]), 'success': False})


class login(generics.CreateAPIView):
	serializer_class = serializers.loginserializer

	def create(self, request, *args, **kwargs):
		try:
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			data = serializer.get_data()			
			return Response({'message': 'login successfully', 'success': True, 'data':data})
			
		except Exception as e:
			return Response({'message': format(e.args[-1]), 'success': False})


class usermaster(generics.CreateAPIView):
	serializer_class = serializers.usermasterserializer
	permission_classes = (IsAuthenticated,)
	model = models.UserMaster

	def post(self, request):
		try:
			a = self.model.objects.create(mobile_number=request.user, profile=request.data['profile'])
			return Response({'message': 'profile added successfully', 'success': True,})
		except Exception as e:
			return Response({'message': format(e.args[-1]), 'success': False})

	def patch(self, request):
		try:
			old_profile = self.models.objects.get(mobile_number=request.user)
			old_profile.profile = request.data['profile']
			old_profile.save()
			return Response({'message': 'profile updated successfully', 'success': True,})
		except Exception as e:
			return Response({'message': format(e.args[-1]), 'success': False})


class logout(generics.GenericAPIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		try:
			auth.logout(request)
			return Response({'message': 'logout successfully', 'success':True})
		except Exception as e:
			return Response({'message': format(e.args[-1]), 'success':False})