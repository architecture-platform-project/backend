from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, ErrorDetail

from user.models import User


class CustomRegisterSerializer(RegisterSerializer):
    """
    커스텀 회원가입 Serializer
    """

    user_name = serializers.CharField()
    birth_date = serializers.DateField()
    is_architect = serializers.BooleanField(default=False)
    phone_number = PhoneNumberField()
    gender = serializers.ChoiceField(choices=[("m", "Male"), ("f", "Female")])

    class Meta:
        model = User
        fields = [
            "user_name",
            "email",
            "password1",
            "password2",
            "birth_date",
            "phone_number",
            "gender",
        ]

    def custom_signup(self, request, user):
        """
        회원가입 커스텀
        - 유저이름
        -
        """
        user.user_name = self.validated_data["user_name"]
        user.birth_date = self.validated_data["birth_date"]
        user.phone_number = self.validated_data["phone_number"]
        user.gender = self.validated_data["gender"]
        user.save()

    @transaction.atomic
    def save(self, request):
        try:
            return super().save(request)
        except Exception as e:
            transaction.set_rollback(rollback=True)
            raise ValidationError({"detail": e})

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["user_name"] = self.validated_data.get("user_name", "")
        data["birth_date"] = self.validated_data.get("birth_date", "")
        data["is_architect"] = self.validated_data.get("is_architect", "")
        data["phone_numbers"] = self.validated_data.get("phone_numbers", "")
        data["gender"] = self.validated_data.get("gender", "")
        return data
