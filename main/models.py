from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import localdate


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    SUPER_MASTER, MASTER, SLAVE = "Руководитель компании", "Руководитель подразделения", "Работник"
    POSITION_CHOICES = (
        (SUPER_MASTER, _("Руководитель компании")),
        (MASTER, _("Руководитель подразделени")),
        (SLAVE, _("Работник")),
    )

    email = models.EmailField(unique=True)

    name = models.CharField(_("Имя"), max_length=100)
    second_name = models.CharField(_("Отчество"),max_length=100)
    surname = models.CharField(_("Фамилия"),max_length=100)

    position = models.CharField(_("Должность"), choices=POSITION_CHOICES, default=SLAVE, max_length=30)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    date_joined = models.DateTimeField(_("Зарегистрирован"), auto_now_add=True)
    is_active = models.BooleanField(_("Активный"), default=True, help_text=_("Активирован ли аккаунт пользователя"))
    is_staff = models.BooleanField(_("Сотрудник"), default=False, help_text=_("Является ли сотрудником"))

    objects = UserManager()

    def __str__(self):
        return f"{self.surname} {self.name} {self.second_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


def tommorow():
    return timezone.now() + timedelta(days=1)


class Assignment(models.Model):
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name="master")
    slave = models.ForeignKey(User, on_delete=models.CASCADE, related_name="slave")

    name = models.CharField(_("Название поручения"), max_length=255)
    description = models.TextField(_("Описание поручения"))

    date = models.DateField(_("Дата создания"), auto_now=True)
    duration = models.IntegerField(_("Длительность"), help_text=_("В днях"), default=1)
    expiration_date = models.DateField(_("Дата сдачи"), default=tommorow)

    class Meta:
        verbose_name = "Поручение"
        verbose_name_plural = "Поручения"

    def __str__(self):
        return self.name
