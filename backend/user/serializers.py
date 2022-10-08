from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from user.models import User


class CustomRegisterSerializer(RegisterSerializer):
    """
    커스텀 회원가입 Serializer
    """

    age = serializers.IntegerField()
    is_architect = serializers.BooleanField(default=False)
    phone_number = PhoneNumberField()
    gender = serializers.ChoiceField(choices=[("m", "Male"), ("f", "Female")])

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "age",
            "phone_number",
            "gender",
        ]

    def custom_signup(self, request, user):
        user.username = self.validated_data["username"]
        user.age = self.validated_data["age"]
        user.phone_number = self.validated_data["phone_number"]
        user.gender = self.validated_data["gender"]
        user.save()

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["age"] = self.validated_data.get("age", "")
        data["is_architect"] = self.validated_data.get("is_architect", "")
        data["phone_numbers"] = self.validated_data.get("phone_numbers", "")
        data["gender"] = self.validated_data.get("gender", "")
        return data
