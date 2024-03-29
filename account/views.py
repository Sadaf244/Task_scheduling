from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import UserSignupValidation, User, UserOnBoard
from django.http import JsonResponse
import logging
from django.contrib.auth import login
from rest_framework.authtoken.models import Token


class UserSignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            context = {}
            email_address = request.data.get('email_address', None)
            username = request.data.get('user_name', '')

            user_exists = User.is_user_exists(email=email_address, username=username)
            if user_exists:
                return JsonResponse({"status": False, 'message': 'User already registered. Please contact.', 'is_registered': True}, status=400)

            user_on_board = UserOnBoard(request)
            resp_dict, user = user_on_board.start_on_boarding()
            print('hey there is user',user)
            if resp_dict['status']:
                token = User.get_user_token(user)
                context.update({
                    'status': True,
                    'message': 'Congratulations! You have signed up successfully.',
                    'token': token.key,
                    'email': user.email
                })
                return JsonResponse(context, status=201)

        except Exception as e:
            logging.error('Exception on User Signup: %s', repr(e))

        return JsonResponse({"status": False, 'message': 'Unable to create user. Please contact.'}, status=500)


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email and password:
            user = User.objects.authenticate(email, password)
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({
                    'status': True,
                    'message': 'Login successful',
                    'token': token.key,
                    'email': user.email
                })
            else:
                return JsonResponse({'status': False, 'message': 'Invalid credentials'}, status=401)
        else:
            return JsonResponse({'status': False, 'message': 'Both email and password are required'}, status=400)


