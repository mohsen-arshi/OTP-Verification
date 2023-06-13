from rest_framework import serializers
from .models import UserPostModel


class UserLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=13)

    def validate(self, phone: str) -> str:
        if not str(phone)[1:].isnumeric():
            raise serializers.ValidationError("please enter a Valid Number")
        elif not str(phone).startswith("09") or str(phone).startswith("+98"):
            raise serializers.ValidationError("please enter a Valid Number")
        elif len(phone) != 11 or 13:
            raise serializers.ValidationError("please enter a Valid Number")
        return phone


class UserVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=13)
    otp = serializers.CharField(required=False)

    def mobile_validate(self, phone: str) -> str:
        if not str(phone)[1:].isnumeric():
            raise serializers.ValidationError("please enter a Valid Number")
        elif not str(phone).startswith("09") or str(phone).startswith("+989"):
            raise serializers.ValidationError("please enter a Valid Number")
        elif len(phone) != 11 or 13:
            raise serializers.ValidationError("please enter a Valid Number")
        return phone

    def otp_validate(self, otp: str) -> str:
        if len(otp) != 6:
            raise serializers.ValidationError("Please enter a correct password")
        elif not str(otp).isnumeric():
            raise serializers.ValidationError("Please enter a correct password")
        return otp


class UserPostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    text = serializers.CharField(max_length=100)

    class Meta:
        model = UserPostModel
        fields = ('owner', 'title', 'slug', 'text', 'created_at', 'modified_at')
        read_only_fields = ['owner', 'slug', 'created_at', 'modified_at']