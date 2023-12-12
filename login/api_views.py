from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_p.models import Users
from main_p.models import UserRole

class LoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # 处理 POST 请求中的用户名和密码
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        # 使用 Django 的 authenticate 函数验证用户
        user = Users.objects.get(username=username)
        user_id = user.userid
        user_role_object = UserRole.objects.get(userid=user_id)
        user_role = user_role_object.role
        user_role = user_role.lower()
        real_password = user.password

        if user_role == role and password == real_password:
            # 返回成功的响应
            return Response({'message': 'Login successful', 'user_id':user_id}, status=status.HTTP_200_OK)
        else:
            # 如果验证失败，返回错误的响应
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterAPIView(APIView):

    def post(self, request, *args, **kwargs):

        email = request.data.get('eamil')
        username =