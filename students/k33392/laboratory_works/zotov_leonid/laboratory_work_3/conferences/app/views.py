from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin
from django.contrib.auth.models import User
from .models import Conference, Registration, Review, Topic
from . import serializers
from rest_framework.permissions import IsAuthenticated
from . import permissions

class ConfrenceViewSet(viewsets.ModelViewSet):
    # Viewset для модели Conference, позволяющий выполнять различные действия над данными (list, retrieve, create, update, delete)
    queryset = Conference.objects.all()  # Указываем набор объектов для работы с viewset
    permission_classes = [IsAuthenticated]  # Устанавливаем разрешения для доступа к данным

    def get_serializer_class(self):
        # Определяем класс сериализатора в зависимости от выполняемого действия
        if self.action in ['list', 'retrieve']:
            print(1)  # Для отладки: печатаем '1' при выполнении действий list или retrieve
            return serializers.ShowConferenceSerializer  # Используем определенный сериализатор для действий list и retrieve
        return serializers.ConferenceSerializer  # Для других действий используем другой сериализатор

    def perform_create(self, serializer):
        # Выполняем дополнительные действия при создании объекта
        serializer.save(author=self.request.user)  # Устанавливаем автора конференции как текущего пользователя

class TopicViewSet(viewsets.ModelViewSet):
    # Viewset для модели Topic
    queryset = Topic.objects.all()  # Указываем набор объектов для работы с viewset
    serializer_class = serializers.TopicSerializer  # Указываем класс сериализатора

    permission_classes = [IsAuthenticated]  # Устанавливаем разрешения для доступа к данным

class RegistrationViewSet(viewsets.ModelViewSet):
    # Viewset для модели Registration
    queryset = Registration.objects.all()  # Указываем набор объектов для работы с viewset

    def get_permissions(self):
        # Определяем разрешения в зависимости от выполняемого действия
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]  # Для list и retrieve используем разрешения только для аутентифицированных пользователей
        return [IsAuthenticated(), permissions.RegistrationsPermissions()]  # Для других действий добавляем кастомные разрешения

    def get_serializer_class(self):
        # Определяем класс сериализатора в зависимости от выполняемого действия
        if self.action in ['list', 'retrieve']:
            return serializers.ShowRegistrationSerializer  # Используем определенный сериализатор для действий list и retrieve
        return serializers.RegistrationSerializer  # Для других действий используем другой сериализатор

class ReviewViewSet(viewsets.ModelViewSet):
    # Viewset для модели Review
    queryset = Review.objects.all()  # Указываем набор объектов для работы с viewset
    permission_classes = [IsAuthenticated]  # Устанавливаем разрешения для доступа к данным

    def get_serializer_class(self):
        # Определяем класс сериализатора в зависимости от выполняемого действия
        if self.action in ['list', 'retrieve']:
            return serializers.ShowReviewSerializer  # Используем определенный сериализатор для действий list и retrieve
        return serializers.ReviewSerializer  # Для других действий используем другой сериализатор

class ProfileViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    # Viewset для профиля пользователя
    queryset = User.objects.all()  # Указываем набор объектов для работы с viewset
    serializer_class = serializers.ProfileSerilaizer  # Указываем класс сериализатора

    permission_classes = [IsAuthenticated, permissions.ProfilePermissions]
    # Устанавливаем разрешения для доступа к данным пользователя, включая кастомные разрешения
