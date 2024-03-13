#Задание 1

Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей. Задание можете выполнить либо в интерактивном режиме интерпретатора, либо в отдельном python-файле. Результатом должны стать запросы и отображение созданных объектов.

##add_date.py

В коде были реализованы функции сощдания объекта и их последующее использование.

```
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
```

##Вывод результата

![Задание 1](img\task1.png)

#Задание 2

По созданным в пр.1 данным написать следующие запросы на фильтрацию:

Где это необходимо, добавьте related_name к полям модели
Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

##filter.py

В коде были реализованы функции для получения объектов с необходимой фильтрацией и их последующее применение

```
    import os

    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_first_app.settings")
    django.setup()

    from django.utils import timezone
    from blog.models import CustomUser, Auto, Ownership, DrivingLicence

    toyota_cars = Auto.objects.filter(brand="Toyota").all()

    maks_owners = CustomUser.objects.filter(first_name="Максим").all()

    random_owner_id = CustomUser.objects.order_by("?").values_list("id", flat=True).first()
    random_owner_licence = DrivingLicence.objects.get(owner_id=random_owner_id)

    black_car_owners = CustomUser.objects.filter(ownerships__auto__color="черный").all()

    this_year_owners = CustomUser.objects.filter(licences__start_date__year=timezone.now().year).all()


    print(
        f"Автомобили Toyota: {toyota_cars}",
        f"Автовладельцы Максимы: {maks_owners}",
        f"Лицензия случайного автовладельца: {random_owner_licence}",
        f"Владельцы черных автомобилей: {black_car_owners}",
        f"Владельцы, получившие лицензию в этом году: {this_year_owners}",
        sep="\n\n",
    )
```

##Вывод результата

![Задание 2](img\task2.png)

#Задание 3

Необходимо реализовать следующие запросы c применением описанных методов:
Вывод даты выдачи самого старшего водительского удостоверения
Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
Выведите количество машин для каждого водителя
Подсчитайте количество машин каждой марки
Отсортируйте всех автовладельцев по дате выдачи удостоверения (Примечание: чтобы не выводить несколько раз одни и те же таблицы воспользуйтесь методом .distinct()

##aggregate_date.py
В коде были реализованы функции для получения необходимых агрегированных данных и их последующее применение

```
import os
import django
from django.db.models import Min, Max, Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_first_app.settings")
django.setup()
from blog.models import CustomUser, Auto, Ownership, DrivingLicence

def get_oldest_licence_date():
    return DrivingLicence.objects.aggregate(Min("start_date"))['start_date__min']

def get_newest_ownership_date():
    return Ownership.objects.aggregate(Max("start_date"))['start_date__max']

def get_ownerships_counts():
    return CustomUser.objects.annotate(count=Count("ownerships"))

def get_cars_count_by_brands():
    return Auto.objects.values("brand").annotate(count=Count("id"))

def get_sorted_owners():
    return CustomUser.objects.order_by("ownerships__start_date")

oldest_licence = get_oldest_licence_date()
newest_ownership = get_newest_ownership_date()
ownerships_counts = get_ownerships_counts()
cars_count_by_brands = get_cars_count_by_brands()
sorted_owners = get_sorted_owners()

ownerships_counts_str = [f"{owner.full_name}: {owner.count}" for owner in ownerships_counts]
cars_count_by_brands_str = [f"{car['brand']}: {car['count']}" for car in cars_count_by_brands]

print(
    f"Дата самого старшего удостоверения: {oldest_licence}",
    f"Самая поздняя дата авто владения: {newest_ownership}",
    f"Количество машин для каждого водителя: {ownerships_counts_str}",
    f"Количество машин каждой марки: {cars_count_by_brands_str}",
    f"Автовладельцы, отсортированные по дате выдачи удостоверения: {sorted_owners}",
    sep="\n\n",
)

```

##Вывод результата:

![Задание 3](img\task3.png)
