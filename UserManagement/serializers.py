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


class BasicUserDataSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.SerializerMethodField()
    profile_img = serializers.CharField()

    def get_email(self, obj):
        if obj.settings.is_email_public:
            return obj.email
        else:
            return "User's e-mail is private"




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
