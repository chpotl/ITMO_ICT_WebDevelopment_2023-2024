# Лабораторная работа №3

## permissions.py

`

    class ProfilePermissions(BasePermission): # Создание пользовательского класса разрешений, основанного на BasePermission

        def has_object_permission(self, request, view, obj):
            # Определение метода проверки разрешений для объекта
            print(obj)  # Вывести объект для отладки

            # Проверить, равен ли пользователь, отправивший запрос, объекту
            if request.user == obj:
                return True  # Вернуть True, если пользователь имеет доступ к объекту
            return False  # В противном случае вернуть False

    class RegistrationsPermissions(BasePermission): # Создание другого пользовательского класса разрешений, также основанного на BasePermission

        def has_object_permission(self, request, view, obj):
            # Определение метода проверки разрешений для объекта

            # Проверить, является ли пользователь, отправивший запрос, владельцем объекта регистрации
            if request.user == obj.user:
                return True  # Вернуть True, если пользователь имеет доступ к объекту регистрации
            return False  # В противном случае вернуть False

`

## Краткое пояснение

Пермишены в Django REST Framework используются для контроля доступа к объектам и действиям в API. Они определяют, может ли пользователь выполнять определенное действие с объектом.

## serializers.py

`

    class TopicSerializer(serializers.ModelSerializer):
        # Сериализатор для модели Topic
        class Meta:
            model = Topic
            fields = "__all__"  # Включаем все поля модели в сериализацию

    class ConferenceSerializer(serializers.ModelSerializer):
        # Сериализатор для модели Conference
        class Meta:
            model = Conference
            fields = ['title', 'topics', 'location', 'start_date', 'end_date',
                    'description', 'participation_conditions']
        # Определяем, какие поля модели будут сериализованы

    class ShowConferenceSerializer(serializers.ModelSerializer):
        # Сериализатор для модели Conference с дополнительной информацией (например, автор конференции)
        author = serializers.CharField(source='author.username')  # Используем CharField для отображения имени автора
        topics = TopicSerializer(many=True, read_only=True)  # Добавляем сериализатор для связанных тем

        class Meta:
            model = Conference
            fields = ['author', 'title', 'topics', 'location', 'start_date', 'end_date',
                    'description', 'participation_conditions']
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

`

## Крвткое пояснение

Конечная цель сериализаторов в Django REST Framework - преобразование объектов Python (моделей Django) в форматы данных, которые легко обрабатывать через HTTP запросы (например, JSON).

## views.py

`

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
                return [IsAuthenticated]  # Для list и retrieve используем разрешения только для аутентифицированных пользователей
            return [IsAuthenticated, permissions.RegistrationsPermissions]  # Для других действий добавляем кастомные разрешения

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

`
