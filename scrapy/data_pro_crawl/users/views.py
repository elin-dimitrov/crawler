from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import status
from django.contrib.auth import login, logout, authenticate
from . import serializers
from  .models import Users
import datetime
import base64
from datetime import datetime


class UsersSession(APIView):


    @authentication_classes((TokenAuthentication,))
    def post(self, request):

        """This method help to create user account with Token authorization"""
  
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        decoded_pw = base64.b64decode(password)
        try:
            user = Users.objects.get(username=username)
            try:
                token = Token.objects.get(user=username)
            except Token.DoesNotExist:
                token = Token.objects.create(user=username)
        except Users.DoesNotExist:
            user = Users.objects.create(username=username,
                                       password=decoded_pw  ,
                                       email=email)
        token = Token.objects.create(user=user)

        user.last_login = datetime.now()
        user.save()
        login(request, user)
        serialized = serializers.UserSerializer(user, many=False)
        response = {}
        response['token'] = token.key
        response.update(serialized.data)
        return Response(data=response, status=status.HTTP_200_OK)

    @authentication_classes((TokenAuthentication,))
    def get(self, request):

        """This method allowing to get json object wiht all creeated users"""

        users = Users.objects.all()
        serialized = serializers.UserSerializer(users, many=True)
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @authentication_classes((TokenAuthentication,))
    def delete(self, request):

        """This method allowing to logout/delete the curent loged in user"""

        user_id = request.data.get('id')
        try:
            Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response(data={'message': 'Invalid User ID'}, status=status.HTTP_404_NOT_FOUND)
        logout(request)
        return Response(data={'message': 'User has successfully logout'}, status=status.HTTP_200_OK)

    @authentication_classes((TokenAuthentication,))
    def put(self, request):

        """This method allow to change the users data like username or password"""

        username = request.data.get('username', None)
        user_id = request.data.get('id')
        password = request.data.get('password')
        decoded_pw = base64.b64decode(password)
        try:
            user = Users.objects.get(id=user_id)
            user.username=username
            user.password=decoded_pw
        except Users.DoesNotExist:
            return Response(data={'message': 'Invalid User ID'}, status=status.HTTP_404_NOT_FOUND)
        user.save()
        serialized = serializers.UserSerializer(user, many=False)
        return Response(data=serialized.data, status=status.HTTP_200_OK)