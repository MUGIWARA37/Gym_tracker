from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.validators import validate_image_upload
from users.models import PasswordResetToken, User
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "age",
            "height_cm",
            "weight_kg",
            "fitness_goal",
            "role",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "role", "created_at", "updated_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user


class ProfileSerializer(UserSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    def validate_profile_picture(self, value):
        if value is None:
            return value
        return validate_image_upload(value, settings.MAX_UPLOAD_SIZE_MB)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs):
        validate_password(attrs["new_password"], self.context["request"].user)
        return attrs


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        validate_password(attrs["new_password"])
        try:
            reset_token = PasswordResetToken.objects.get(token=attrs["token"], is_used=False)
        except PasswordResetToken.DoesNotExist as exc:
            raise serializers.ValidationError({"token": "Invalid or expired token."}) from exc
        attrs["reset_token"] = reset_token
        return attrs
