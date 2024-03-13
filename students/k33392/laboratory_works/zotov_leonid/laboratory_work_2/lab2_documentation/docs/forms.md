# Формы

# UserRegisterForm

## Код

`class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']`

## Описание

Форма регистрации пользователя на сайте. Эта форма наследует функциональность от UserCreationForm, но также добавляет поле email.

## Поля

- username: Имя пользователя.
- email: Электронная почта пользователя.
- password1: Пароль.
- password2: Подтверждение пароля.

# ConferenceForm

## Код

`class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['title', 'topics', 'location', 'start_date', 'end_date', 'description', 'participation_conditions']`

## Описание

Форма для создания или редактирования конференций.

## Поля

- title: Название конференции.
- topics: Темы, которые будут обсуждаться на конференции.
- location: Место проведения конференции.
- start_date: Дата начала конференции.
- end_date: Дата окончания конференции.
- description: Описание конференции.
- participation_conditions: Условия участия в конференции.

# ReviewForm

## Код

`class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']`

## Описание

Форма для создания или редактирования отзывов о конференции.

## Поля

- text: Текст отзыва.
- rating: Оценка конференции (например, от 1 до 5).

# RegistrationForm

## Код

`class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = []`

## Описание

Форма для регистрации пользователя на конференцию.

## Поля

В этом случае, нет полей для отображения, так как всё необходимое автоматически добавляется.
