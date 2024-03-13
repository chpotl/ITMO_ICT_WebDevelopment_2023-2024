from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conference, Registration, Review, Topic
# Импортируем необходимые модули и модели из Django и Django REST Framework

class TopicSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Topic
    class Meta:
        model = Topic
        fields = "__all__"  # Включаем все поля модели в сериализацию

class ConferenceSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Conference
    class Meta:
        model = Conference
        fields = "__all__"
    # Определяем, какие поля модели будут сериализованы

class ShowConferenceSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Conference с дополнительной информацией (например, автор конференции)
    author = serializers.CharField(source='author.username')  # Используем CharField для отображения имени автора
    topics = TopicSerializer(many=True, read_only=True)  # Добавляем сериализатор для связанных тем

    class Meta:
        model = Conference
        fields = "__all__"
    # Определяем, какие поля модели будут сериализованы, включая дополнительную информацию

class RegistrationSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Registration
    class Meta:
        model = Registration
        fields = "__all__"  # Включаем все поля модели в сериализацию

class ShowRegistrationSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Registration с дополнительной информацией (например, связанные объекты)
    conference = ShowConferenceSerializer(read_only=True)  # Сериализатор для связанной конференции
    topic = TopicSerializer(read_only=True)  # Сериализатор для связанной темы

    class Meta:
        model = Registration
        fields = ['user', 'conference', 'topic', 'is_approved']
    # Определяем, какие поля модели будут сериализованы, включая дополнительную информацию

class ReviewSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Review
    class Meta:
        model = Review
        fields = '__all__'  # Включаем все поля модели в сериализацию

class ShowReviewSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Review с дополнительной информацией (например, связанные объекты)
    conference = ShowConferenceSerializer(read_only=True)  # Сериализатор для связанной конференции

    class Meta:
        model = Review
        fields = ['conference', 'text', 'user', 'comment_date', 'comment_text', 'rating']
    # Определяем, какие поля модели будут сериализованы, включая дополнительную информацию

class ProfileSerilaizer(serializers.ModelSerializer):
    # Сериализатор для модели User (профиль пользователя)
    authored_conferences = ShowConferenceSerializer(many=True, read_only=True)  # Сериализатор для конференций, созданных пользователем
    registered_in = ShowRegistrationSerializer(many=True, read_only=True)  # Сериализатор для регистраций пользователя на конференции
    user_reviews = ShowReviewSerializer(many=True, read_only=True)  # Сериализатор для отзывов пользователя

    class Meta:
        model = User
        fields = ['username', 'authored_conferences', 'registered_in', 'user_reviews']
    # Определяем, какие поля модели будут сериализованы, включая дополнительную информацию о конференциях, регистрациях и отзывах пользователя
