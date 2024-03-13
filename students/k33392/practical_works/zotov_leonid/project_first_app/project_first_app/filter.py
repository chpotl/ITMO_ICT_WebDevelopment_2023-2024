import os
import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_first_app.settings")
django.setup()
from blog.models import CustomUser, Auto, DrivingLicence

def get_toyota_cars():
    return Auto.objects.filter(brand="Toyota")

def get_users_named_maxim():
    return CustomUser.objects.filter(first_name="Максим")

def get_random_user_licence():
    random_owner_id = CustomUser.objects.order_by("?").values_list("id", flat=True).first()
    return DrivingLicence.objects.get(owner_id=random_owner_id)

def get_black_car_owners():
    return CustomUser.objects.filter(ownerships__auto__color="черный")

def get_this_year_licence_owners():
    return CustomUser.objects.filter(licences__start_date__year=timezone.now().year)

toyota_cars = get_toyota_cars()
maks_owners = get_users_named_maxim()
random_owner_licence = get_random_user_licence()
black_car_owners = get_black_car_owners()
this_year_owners = get_this_year_licence_owners()

print(
    f"Автомобили Toyota: {toyota_cars}",
    f"Автовладельцы Максимы: {maks_owners}",
    f"Лицензия случайного автовладельца: {random_owner_licence}",
    f"Владельцы черных автомобилей: {black_car_owners}",
    f"Владельцы, получившие лицензию в этом году: {this_year_owners}",
    sep="\n\n",
)
