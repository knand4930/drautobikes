from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django_otp import devices_for_user
# from pyotp import TOTP
# from .serializers import RegisterSerializer, LoginSerializer
from .models import *
from rest_framework.decorators import api_view
from .utils import *


# Create your views here.

@api_view(['POST'])
def send_otp(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': "Key Phone_number is Required!"
        })

    if data.get('phone_number') is None:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "key password is required!"
        })

    user = User.objects.create(phone_number=data.get('phone_number'),
                               otp=send_otp_to_phone(data.get('phone_number')))
    user.set_password = data.get('password')
    user.save()

    return Response({
        'status': status.HTTP_200_OK,
        'messages': 'OTP Sent '
    })


@api_view(['POST'])
def verify_otp(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': "Key Phone_number is Required!"
        })

    if data.get('otp') is None:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': "key otp is required !"
        })

    try:
        user_obj = User.objects.get(phone_number=data.get('phone_number'))

    except Exception as e:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Invalid otp'
        })

    if user_obj.otp == data.get('otp'):
        user_obj.is_phone_verified = True
        user_obj.save()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'otp matched'
        })
    return Response({
        'status': status.HTTP_400_BAD_REQUEST,
        'message': "Invalid Phone Number!"
    })

#
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             totp_device = devices_for_user(user)[0]
#             if totp_device.verify(serializer.data['otp']):
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.contrib.auth import get_user_model, authenticate
# from django.core.exceptions import ObjectDoesNotExist
# from django.utils.crypto import get_random_string
# from django.core.cache import cache
#
# User = get_user_model()
#
#
# @api_view(['POST'])
# def register(request):
#     phone_number = request.data.get('phone_number')
#     otp = request.data.get('otp')
#     password = request.data.get('password')
#     try:
#         user = User.objects.get(phone_number=phone_number)
#         return Response({'error': 'User with this phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
#     except ObjectDoesNotExist:
#         pass
#     if not otp:
#         return Response({'error': 'Please provide OTP to register.'}, status=status.HTTP_400_BAD_REQUEST)
#     if not password:
#         return Response({'error': 'Please provide Password to register.'}, status=status.HTTP_400_BAD_REQUEST)
#     if not validate_otp(phone_number, otp):
#         return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
#     user = User.objects.create_user(phone_number=phone_number, password=password)
#     return Response({'success': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#
#
# @api_view(['POST'])
# def login(request):
#     phone_number = request.data.get('phone_number')
#     otp = request.data.get('otp')
#     if not otp:
#         return Response({'error': 'Please provide OTP to login.'}, status=status.HTTP_400_BAD_REQUEST)
#     user = authenticate(request=request, username=phone_number, password=otp)
#     if user:
#         return Response({'success': 'User authenticated successfully'}, status=status.HTTP_200_OK)
#     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#
#
# def generate_otp():
#     return get_random_string(length=6, allowed_chars='0123456789')
#
#
# def send_otp(phone_number, otp):
#     # Implement your code to send OTP to the user's phone number here
#     # For example, you could use a third-party SMS gateway service
#     # and send the OTP via SMS to the user's phone number
#     # This implementation is outside the scope of this example
#     pass
#
#
# def validate_otp(phone_number, otp):
#     cached_otp = cache.get(phone_number)
#     if cached_otp and cached_otp == otp:
#         cache.delete(phone_number)
#         return True
#     return False
#
#
# @api_view(['POST'])
# def send_otp(request):
#     phone_number = request.data.get('phone_number')
#     try:
#         user = User.objects.get(phone_number=phone_number)
#     except ObjectDoesNotExist:
#         return Response({'error': 'User with this phone number does not exist'}, status=status.HTTP_400_BAD_REQUEST)
#     otp = generate_otp()
#     print(otp)
#     send_otp(phone_number, otp)
#     cache.set(phone_number, otp, timeout=300)
#     return Response({'success': 'OTP sent successfully'}, status=status.HTTP_200_OK)
