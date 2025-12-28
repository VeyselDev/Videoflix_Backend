from typing import Dict, Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField

from app_auth.models import CustomUser
from app_auth.utils.password_utils import validate_passwords_match


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'confirmed_password']
        read_only_fields = ['id']

    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="This email already exists.")])
    password = PasswordField()
    confirmed_password = PasswordField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        validate_passwords_match(attrs['password'], attrs['confirmed_password'])
        validate_password(attrs['password'])

        validated_data = attrs.copy()
        validated_data.pop('confirmed_password')
        return validated_data


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        validated_data = super().validate(attrs)
        validated_data['user'] = UserSerializer(self.user).data
        return validated_data


class PasswordChangeSerializer(serializers.Serializer):
    new_password = PasswordField()
    confirmed_password = PasswordField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        validate_passwords_match(attrs['new_password'], attrs['confirmed_password'])
        validate_password(attrs['new_password'])
        return attrs
