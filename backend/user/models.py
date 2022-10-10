from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


from phonenumber_field.modelfields import PhoneNumberField

from common.models import TimeStampModel


class UserManager(BaseUserManager):
    """유저매니저 재정의"""

    def _create_user(
        self,
        user_name,
        email,
        password,
        phone_number,
        gender,
        birth_date,
        is_architect,
        **extra_fields
    ):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.user_name = user_name
        user.phone_number = phone_number
        user.gender = gender
        user.birth_date = birth_date
        user.is_architect = is_architect
        user.save()

        return user

    def create_user(self, user_name, email, password, **extra_fields):
        return self._create_user(user_name, email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class Corporation(models.Model):
    """회사법인 모델"""

    business_name = models.CharField(_("상호명"), max_length=45)
    repr_name = models.CharField(_("대표자명"), max_length=45)
    business_address = models.CharField(_("사업장 주소"), max_length=300)
    homepage_url = models.CharField(_("Homepage"), max_length=300)
    business_reg_num = models.CharField(_("사업자 등록 번호"), max_length=12)
    office_op_num = models.CharField(_("사무소 개설 번호"), max_length=10)

    class Meta:
        db_table = "corporations"

    def __str__(self):
        return self.business_name


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    """유저 모델"""

    username_validator = UnicodeUsernameValidator()

    user_name = models.CharField(_("user_name"), max_length=45, unique=False)
    email = models.EmailField(_("email_address"), unique=True)
    phone_number = PhoneNumberField(null=True, unique=True)
    is_architect = models.BooleanField(_("Is architect"), default=False, null=False)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    gender = models.CharField(
        max_length=1, choices=[("m", "Male"), ("f", "Female")], null=True
    )
    birth_date = models.DateField(null=True)
    corporation = models.OneToOneField(
        Corporation, null=True, on_delete=models.SET_NULL
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
