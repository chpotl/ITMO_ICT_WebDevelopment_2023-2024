import os
from datetime import datetime
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_first_app.settings")
import django
django.setup()

from blog.models import CustomUser, Auto, Ownership, DrivingLicence

def create_users():
    user_data = [
        {"last_name": "Зотов", "first_name": "Леонид"},
        {"last_name": "Болотов", "first_name": "Игорь"},
        {"last_name": "Михайлушкин", "first_name": "Георгий"},
        {"last_name": "Круглова", "first_name": "Ольга"},
        {"last_name": "Васильев", "first_name": "Александр"},
        {"last_name": "Дмитриева", "first_name": "Александра"},
    ]
    return [CustomUser(last_name=user['last_name'], first_name=user['first_name'], birthdate=datetime.now()) for user in user_data]

def create_cars():
    car_data = [
        {"state_number": "F457CC70", "brand": "Haval", "model": "Jolion", "color": "красный"},
        {"state_number": "Q128IU70", "brand": "Lada", "model": "Kalina", "color": "синий"},
        {"state_number": "J094JK70", "brand": "Foed", "model": "Mustang", "color": "жёлтый"},
        {"state_number": "J568RF70", "brand": "Hyundai", "model": "Solaris", "color": "чёрный"},
        {"state_number": "S271NK70", "brand": "Skoda", "model": "Octavia", "color": "серый"},
        {"state_number": "C027WE70", "brand": "Toyota", "model": "Outlander", "color": "бирёзовый"},
    ]
    return [Auto(**car) for car in car_data]

def create_relationships(owners, cars):
    return [Ownership(owner=owners[i], auto=cars[i], start_date=datetime.now()) for i in range(len(owners))]

def create_licences(owners):
    return [DrivingLicence(owner=owner, number=str(index + 1) * 10, type="B", start_date=datetime.now()) for index, owner in enumerate(owners)]

owners = create_users()
cars = create_cars()
ownerships = create_relationships(owners, cars)
licences = create_licences(owners)

CustomUser.objects.bulk_create(owners)
Auto.objects.bulk_create(cars)
Ownership.objects.bulk_create(ownerships)
DrivingLicence.objects.bulk_create(licences)

print("Автовладельцы:")
for owner in owners:
    print(f"{owner.last_name} {owner.first_name} - {owner.birthdate}")

print("\nАвтомобили:")
for car in cars:
    print(f"{car.brand} {car.model} ({car.state_number})")

print("\nВладения:")
for ownership in ownerships:
    print(f"{ownership.owner.last_name} {ownership.owner.first_name} владеет {ownership.auto.brand} {ownership.auto.model}")

print("\nЛицензии:")
for licence in licences:
    print(f"{licence.owner.last_name} {licence.owner.first_name} - {licence.number}")
