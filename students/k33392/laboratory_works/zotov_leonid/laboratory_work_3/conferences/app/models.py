from django.contrib.auth.models import User
from django.db import models


class Conference(models.Model):
    author = models.ForeignKey(User, related_name='authored_conferences', on_delete=models.CASCADE,
                               null=True, blank=True)  # Создатель конференции
    title = models.CharField(max_length=200)  # Название конференции
    topics = models.ManyToManyField('Topic', related_name='in_conferences', blank=True)  # Темы конференции
    location = models.TextField()  # Место проведения конференции
    start_date = models.DateField()  # Дата начала конференции
    end_date = models.DateField()  # Дата окончания конференции
    description = models.TextField()  # Описание конференции
    participation_conditions = models.TextField()  # Условия участия в конференции

    def __str__(self):
        return self.title


class Topic(models.Model):
    name = models.CharField(max_length=100)  # Название темы

    def __str__(self):
        return self.name


class Registration(models.Model):
    user = models.ForeignKey(User, related_name='registered_in', on_delete=models.CASCADE)  # Пользователь, который регистрируется
    conference = models.ForeignKey(Conference, related_name='users_registered', on_delete=models.CASCADE)  # Конференция, на которую регистрируется пользователь
    topic = models.ForeignKey(Topic, related_name='performed_in', on_delete=models.CASCADE, null=True, blank=True)  # Тема выступления пользователя
    is_approved = models.BooleanField(default=False)  # Статус одобрения регистрации

    class Meta:
        unique_together = ('user', 'conference', 'topic')  # Уникальность комбинации

    def __str__(self):
        return f"{self.user.username} - {self.conference.title}"


class Review(models.Model):
    conference = models.ForeignKey(Conference, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)  # Основной текст отзыва
    user = models.ForeignKey(User, related_name='user_reviews', on_delete=models.CASCADE)  # Пользователь, оставивший отзыв
    comment_date = models.DateField(auto_now_add=True)  # Дата создания отзыва
    comment_text = models.TextField()  # Детальный текст комментария к отзыву
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)])  # Оценка конференции от 1 до 10

    def __str__(self):
        return f"{self.user.username} - {self.conference.title} - {self.rating}/10"
