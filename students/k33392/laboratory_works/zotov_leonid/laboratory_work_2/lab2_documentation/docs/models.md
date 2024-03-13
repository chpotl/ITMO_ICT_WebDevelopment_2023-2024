# Модели

# class Conference

## Код

`class Conference(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    topics = models.ManyToManyField('Topic')
    location = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    participation_conditions = models.TextField()`

## Описание

Модель представляет собой конференцию, которую создал пользователь.

## Поля

- author: Ссылка на пользователя, который создал конференцию. Это внешний ключ к модели User.
- title: Название конференции.
- topics: Множественное поле связи, содержащее темы, обсуждаемые на конференции.
- location: Местоположение проведения конференции.
- start_date: Дата начала конференции.
- end_date: Дата завершения конференции.
- description: Подробное описание конференции.
- participation_conditions: Условия участия в конференции.

# class Topic

## Код

`class Topic(models.Model):
    name = models.CharField(max_length=100)`

## Описание

Модель представляет собой тему, которая может быть обсуждаема на конференции.

## Поля

- name: Название темы.

# class UserProfile

## Код

`class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)`

## Описание

Дополнительный профиль для пользователя, расширяющий стандартную модель User.

## Поля

- user: Ссылка на основной профиль пользователя. Это один-к-одному поле связи с моделью User

# class Registration

## Код

`class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)`

## Описание

Модель, представляющая регистрацию пользователя на конкретную конференцию

## Поля

- user: Ссылка на пользователя, который регистрируется.
- conference: Ссылка на конференцию, на которую регистрируется пользователь.
- topic: Тема, с которой пользователь хочет выступить.
- is_approved: Флаг, указывающий, была ли регистрация одобрена.

# class Review

## Код

`class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateField(auto_now_add=True)
    comment_text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)])`

## Описание

Модель, представляющая отзыв пользователя о конференции.

## Поля

- conference: Ссылка на конференцию, к которой относится отзыв.
- text: Текст отзыва.
- user: Ссылка на пользователя, который оставил отзыв.
- comment_date: Дата, когда был оставлен отзыв.
- comment_text: Детальный текст комментария.
- rating: Оценка конференции пользователем от 1 до 10.
