from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission


class CustomUser(models.Model):
    class Meta:
        db_table = "custom_user"
        verbose_name = "Пользователь"

    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    birthdate = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    passport_number = models.CharField(max_length=15, verbose_name="Номер паспорта")
    home_address = models.TextField(verbose_name="Домашний адрес")
    nationality = models.CharField(max_length=30, verbose_name="Национальность")

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    full_name.fget.short_description = "Фамилия и Имя"

    def __str__(self):
        return self.full_name


class Auto(models.Model):
    class Meta:
        db_table = "auto"
        verbose_name = "автомобиль"

    state_number = models.CharField(max_length=15, verbose_name="Государственный номер")
    brand = models.CharField(max_length=20, verbose_name="Марка")
    model = models.CharField(max_length=20, verbose_name="Модель")
    color = models.CharField(max_length=30, verbose_name="Цвет")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.state_number})"


class Ownership(models.Model):
    class Meta:
        db_table = "ownership"
        verbose_name = "владение"

    owner = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Владелец", related_name="ownerships"
    )
    auto = models.ForeignKey(
        Auto, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Автомобиль", related_name="ownerships"
    )
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата конца")

    def __str__(self):
        return f"{self.owner} - {self.auto}"


class DrivingLicence(models.Model):
    class Meta:
        db_table = "driving_licence"
        verbose_name = "водительское удостоверение"

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Владелец", related_name="licences")
    number = models.CharField(max_length=10, verbose_name="Номер удостоверения")
    type = models.CharField(max_length=10, verbose_name="Тип")
    start_date = models.DateTimeField(verbose_name="Дата выдачи")

    def __str__(self):
        return f"{self.owner} ({self.number})"
