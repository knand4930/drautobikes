from rest_framework import serializers
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import authenticate
from pyotp import TOTP

from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ('phone_number',)

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            totp = TOTP('mysecretkey')  # Replace 'mysecretkey' with your own secret key
            user.totp_secret = totp.secret
            user.save()
            totp_device = TOTPDevice.objects.create(user=user, name='default')
            totp_device.save()
            totp_device.generate_challenge()
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        user = authenticate(username=phone_number, otp=otp)
        if not user:
            raise serializers.ValidationError("Invalid phone number or OTP.")
        return user
