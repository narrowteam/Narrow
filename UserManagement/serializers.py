from rest_framework import serializers
from .models import User, UserSettings
import django.contrib.auth.password_validation as validators
from cdn.models import ProfileImage


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

# Data visible to all users

class BasicUserDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    profile_img = serializers.ImageField(read_only=True)

    def get_email(self, obj):
        if obj.settings.is_email_public:
            return obj.email
        else:
            return "User's e-mail is private"


class UserSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSettings
        fields = ('email_notifications_on_events',)

# Detailed data about user, should only be seen by account owner

class UserPatchSerializer(serializers.ModelSerializer):
    settings = UserSettingsSerializer(required=False)

    class Meta:
        model = User
        fields = ('settings', )
        extra_kwargs = {
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.update_user(**validated_data)
        return instance


class UserSetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={'input_type': 'current_password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def save(self):
        user = self.context.get("user")
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

    def validate_new_password(self, data):
        validators.validate_password(password=data, user=User)
        user = self.context.get("user")
        if user.check_password(data):
            raise serializers.ValidationError("New password must be different")
        return data

    def validate_current_password(self, data):
        user = self.context.get("user")
        if not user.check_password(data):
            raise serializers.ValidationError("Wrong password")


class ImageUploadSerializer(serializers.Serializer):
    profile_image = serializers.ImageField(required=True)

    def update(self, instance, validated_data):
        try:
            img = instance.profileImage
            img.update(**validated_data)
        except ProfileImage.DoesNotExist:
            ProfileImage.objects.create(instance, **validated_data)
        return instance


