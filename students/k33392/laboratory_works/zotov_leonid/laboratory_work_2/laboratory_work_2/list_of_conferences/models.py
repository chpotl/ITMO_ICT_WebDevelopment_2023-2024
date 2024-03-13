from django.contrib.auth.models import User
from django.db import models

# Модель для представления конференции.
class Conference(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Создатель конференции
    title = models.CharField(max_length=200)  # Название конференции
    topics = models.ManyToManyField('Topic')  # Темы конференции
    location = models.TextField()  # Место проведения конференции
    start_date = models.DateField()  # Дата начала конференции
    end_date = models.DateField()  # Дата окончания конференции
    description = models.TextField()  # Описание конференции
    participation_conditions = models.TextField()  # Условия участия в конференции

    def __str__(self):
        return self.title

# Модель для представления темы обсуждения на конференции.
class Topic(models.Model):
    name = models.CharField(max_length=100)  # Название темы

    def __str__(self):
        return self.name

# Дополнительный профиль пользователя.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Основная учетная запись пользователя

    def __str__(self):
        return self.user.username

# Модель для представления регистрации пользователя на конференцию.
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, который регистрируется
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)  # Конференция, на которую регистрируется пользователь
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)  # Тема выступления пользователя
    is_approved = models.BooleanField(default=False)  # Статус одобрения регистрации

    class Meta:
        unique_together = ('user', 'conference', 'topic')  # Уникальность комбинации

    def __str__(self):
        return f"{self.user.username} - {self.conference.title}"

# Модель для представления отзывов о конференции.
class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)  # Конференция, к которой относится отзыв
    text = models.TextField(null=True, blank=True)  # Основной текст отзыва
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, оставивший отзыв
    comment_date = models.DateField(auto_now_add=True)  # Дата создания отзыва
    comment_text = models.TextField()  # Детальный текст комментария к отзыву
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)])  # Оценка конференции от 1 до 10

    def __str__(self):
        return f"{self.user.username} - {self.conference.title} - {self.rating}/10"
