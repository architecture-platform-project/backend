from abc import ABC

from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import User, Corporation


class CorporationSerializer(serializers.ModelSerializer):
    """
    Corporation Serializer
    """

    class Meta:
        model = Corporation
        fields = "__all__"


class CustomRegisterSerializer(RegisterSerializer):
    """
    커스텀 회원가입 Serializer
    """

    user_name = serializers.CharField()
    birth_date = serializers.DateField()
    is_architect = serializers.BooleanField(default=False)
    phone_number = serializers.CharField(max_length=20)
    gender = serializers.ChoiceField(choices=[("m", "Male"), ("f", "Female")])
    corporation = CorporationSerializer(many=False, default=None)

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

    def data(self):
        print("data ::::")

    def validated_data(self):
        print("validated data: ")

    def validate(self, data):
        print("validate")
        print("validate data : ", data)
        print("files : ", self.context["request"].FIES)
        print("data : ", self.context["request"].data)

    # Todo: 국제번호도 받게 해야됨
    def validate_phone_number(self, phone_number):
        """
        핸드폰 번호 유효성 검사
        - 010-0000-0000 형식으로만 허용
        :param phone_number:
        :return: +8210-------- 으로 변환
        """
        phone_number_list = phone_number.split("-")
        if (
            phone_number_list[0] != "010"
            or len(phone_number_list[1]) != 4
            or len(phone_number_list[2]) != 4
        ):
            raise ValidationError("010-0000-0000 형식으로 phone_number를 입력해주세요.")
        return "+8210" + phone_number_list[1] + phone_number_list[2]

    def custom_signup(self, request, user):
        """
        회원가입 커스텀
        - 유저이름
        - 생년월일(나이)
        - 핸드폰 번호
        - 성별
        """
        user.user_name = self.validated_data["user_name"]
        user.birth_date = self.validated_data["birth_date"]
        user.phone_number = self.validated_data["phone_number"]
        user.gender = self.validated_data["gender"]
        user.save()

        raise ValidationError({"detail": "eeeee"})

    @transaction.atomic
    def save(self, request):
        print(self.validated_data)
        try:
            return super().save(request)
        except Exception as e:
            transaction.set_rollback(rollback=True)
            raise ValidationError({"detail": e})

    def get_cleaned_data(self):
        print("get cline")
        data = super().get_cleaned_data()
        data["user_name"] = self.validated_data.get("user_name", "")
        data["birth_date"] = self.validated_data.get("birth_date", "")
        data["is_architect"] = self.validated_data.get("is_architect", "")
        data["phone_numbers"] = self.validated_data.get("phone_numbers", "")
        data["gender"] = self.validated_data.get("gender", "")
        data["corporation"] = self.validated_data.get("corporation", "")
        return data


class EmailUniqueCheckSerializer(serializers.ModelSerializer):
    """
    이메일 중복 확인 Serializer
    """

    class Meta:
        model = User
        fields = ["email"]
