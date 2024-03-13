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

Вывод в консоль:

![Задание 3](img\task3.png)
