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
