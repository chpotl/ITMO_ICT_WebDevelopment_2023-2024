from django.contrib import admin
from .models import CustomUser, Auto, Ownership, DrivingLicence


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "passport_number", "home_address", "nationality")
    search_fields = ("last_name", "first_name")


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ("state_number", "brand", "model", "color")
    search_fields = ("number", "brand", "model", "color")
    list_filter = ["brand", "model", "color"]


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ("get_owner", "get_auto", "start_date", "end_date")
    search_fields = (
    "owner__last_name", "owner__first_name", "auto__number", "auto__brand", "auto__model", "auto__color")
    list_filter = ["auto__brand", "auto__model", "auto__color"]

    @admin.display(ordering="owner__last_name", description="Владелец")
    def get_owner(self, obj):
        return f"{obj.owner}"

    @admin.display(ordering="auto__brand", description="Автомобиль")
    def get_auto(self, obj):
        return f"{obj.auto}"


@admin.register(DrivingLicence)
class DrivingLicenceAdmin(admin.ModelAdmin):
    list_display = ("get_owner", "number", "type", "start_date")
    search_fields = ("owner__last_name", "owner__first_name", "number", "type")
    list_filter = ["type"]

    @admin.display(ordering="owner__last_name", description="Владелец")
    def get_owner(self, obj):
        return f"{obj.owner}"
