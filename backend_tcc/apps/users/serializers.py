from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "institutional_email",
            "role",
            "is_active",
            "must_change_password",
            "date_joined",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "institutional_email",
            "role",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None) or "123456"
        # Quando um admin cadastra um professor, a senha definida aqui é uma senha
        # provisória. O professor é obrigado a trocá-la no primeiro login.
        validated_data.setdefault("must_change_password", True)
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
            # Senha redefinida pelo admin -> professor deve trocar de novo no próximo login.
            if instance.role == "professor":
                instance.must_change_password = True
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_new_password(self, value):
        # Reaproveita validadores configurados no settings (se houver).
        validate_password(value)
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    institutional_email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_new_password(self, value):
        validate_password(value)
        return value
