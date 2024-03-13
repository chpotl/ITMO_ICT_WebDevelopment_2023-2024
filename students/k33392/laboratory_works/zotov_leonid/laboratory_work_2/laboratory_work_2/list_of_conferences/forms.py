from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Conference, Review, Registration

# Форма регистрации пользователя.
class UserRegisterForm(UserCreationForm):
    # Дополнительное поле email, так как стандартная форма UserCreationForm не содержит его.
    email = forms.EmailField()

    class Meta:
        # Определение модели, с которой связана форма.
        model = User
        # Поля, которые будут отображаться в форме.
        fields = ['username', 'email', 'password1', 'password2']

# Форма создания/редактирования конференции.
class ConferenceForm(forms.ModelForm):
    class Meta:
        # Определение модели, с которой связана форма.
        model = Conference
        # Поля, которые будут отображаться в форме.
        fields = ['title', 'topics', 'location', 'start_date', 'end_date', 'description', 'participation_conditions']

# Форма создания/редактирования отзыва.
class ReviewForm(forms.ModelForm):
    class Meta:
        # Определение модели, с которой связана форма.
        model = Review
        # Поля, которые будут отображаться в форме.
        fields = ['text', 'rating']

# Форма регистрации на конференцию.
class RegistrationForm(forms.ModelForm):
    class Meta:
        # Определение модели, с которой связана форма.
        model = Registration
        # Поля, которые будут отображаться в форме.
        # В этом случае, нет полей для отображения, так как возможно всё необходимое автоматически добавляется.
        fields = []

