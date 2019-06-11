from rest_framework import serializers
from .models import User, UserSettings
import django.contrib.auth.password_validation as validators

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name',
                  'last_name', 'profile_img', 'password')
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate_password(self, data):
        validators.validate_password(password=data, user=User)
        return data


class UserSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSettings
        fields = ('email_notifications_on_events',)


class UserPatchSerializer(serializers.ModelSerializer):
    settings = UserSettingsSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name',
                  'last_name', 'profile_img', 'settings')
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'profile_img': {'required': False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.update_user(**validated_data)
        return instance



class UserSetPasswordSerializer(UserSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        return instance

    def validate_password(self, data):
        validators.validate_password(password=data, user=User)
        return data
