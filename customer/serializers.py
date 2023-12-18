from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.settings import CHAT_URL


class CustomerSerializer(serializers.ModelSerializer):

    notifications_chat = serializers.URLField(default=CHAT_URL, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id",
                  "email",
                  "first_name",
                  "last_name",
                  "password",
                  "is_staff",
                  "notifications_chat",)
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
