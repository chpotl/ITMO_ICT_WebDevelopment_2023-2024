from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, ConferenceForm, ReviewForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Conference, Review, Registration
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Главная страница.
def index(request):
    # Получаем все доступные конференции.
    conferences = Conference.objects.all()

    # Создаем словарь для отображения участников каждой конференции.
    participants_per_conference = {}
    for conf in conferences:
        # Для каждой конференции извлекаем участников.
        participants = Registration.objects.filter(conference=conf)
        participants_per_conference[conf] = participants

    # Возвращаем страницу с переданными данными.
    return render(request, 'index.html', {
        'conferences': conferences,
        'participants_per_conference': participants_per_conference
    })

# Регистрация нового пользователя.
def register(request):
    # Проверяем, был ли отправлен POST-запрос.
    if request.method == 'POST':
        # Создаем форму с данными из запроса.
        form = UserRegisterForm(request.POST)
        # Проверяем валидность данных.
        if form.is_valid():
            # Сохраняем пользователя и перенаправляем на страницу входа.
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}! Теперь вы можете войти в систему.')
            return redirect('login')
    else:
        # Если запрос не POST, создаем пустую форму.
        form = UserRegisterForm()

    # Возвращаем страницу регистрации с формой.
    return render(request, 'registration/register.html', {'form': form})

# Вход пользователя.
def user_login(request):
    # Проверяем, был ли отправлен POST-запрос.
    if request.method == 'POST':
        # Извлекаем данные из формы входа.
        username = request.POST['username']
        password = request.POST['password']

        # Пытаемся аутентифицировать пользователя.
        user = authenticate(request, username=username, password=password)
        # Если пользователь найден и данные верны, логиним его.
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Иначе выводим сообщение об ошибке.
            messages.error(request, 'Неправильное имя пользователя или пароль')
    # Возвращаем страницу входа.
    return render(request, 'registration/login.html')

# Главная страница авторизованного пользователя.
@login_required  # Требуется вход.
def home(request):
    # Извлекаем конференции, созданные текущим пользователем.
    user_conferences = Conference.objects.filter(author=request.user)
    # Извлекаем все остальные конференции.
    other_conferences = Conference.objects.exclude(author=request.user)

    # Возвращаем страницу с переданными данными.
    return render(request, 'home.html', {
        'user_conferences': user_conferences,
        'other_conferences': other_conferences,
    })

# Страница создания конференции.
@login_required
def create_conference(request):
    # Проверяем, является ли запрос POST-запросом.
    if request.method == 'POST':
        # Инициализируем форму данными из запроса.
        form = ConferenceForm(request.POST)
        # Проверяем валидность данных формы.
        if form.is_valid():
            # Сохраняем данные формы в объект, но ещё не коммитим в базу данных.
            conference = form.save(commit=False)
            # Устанавливаем автора конференции текущим пользователем.
            conference.author = request.user
            # Сохраняем конференцию в базу данных.
            conference.save()
            # Перенаправляем пользователя на главную страницу.
            return redirect('home')
    else:
        # Если запрос не POST, инициализируем пустую форму.
        form = ConferenceForm()

    # Формируем контекст для передачи данных на страницу.
    context = {
        'form': form
    }
    # Рендерим страницу с переданным контекстом.
    return render(request, 'create_conference.html', context)

# Страница редактирования конференции.
@login_required
def edit_conference(request, conference_id):
    # Получаем объект конференции или возвращаем 404 ошибку, если такого объекта нет.
    conference = get_object_or_404(Conference, id=conference_id)
    
    # Проверяем, является ли текущий пользователь автором конференции.
    if request.user != conference.author:
        # Если пользователь не автор, возвращаем ошибку 403.
        return HttpResponseForbidden("You don't have permission to edit this conference.")

    # Проверяем, является ли запрос POST-запросом.
    if request.method == 'POST':
        # Инициализируем форму данными из запроса и текущим объектом конференции.
        form = ConferenceForm(request.POST, instance=conference)
        # Проверяем валидность данных формы.
        if form.is_valid():
            # Сохраняем изменения.
            form.save()
            # Перенаправляем пользователя на главную страницу.
            return redirect('home')
    else:
        # Если запрос не POST, инициализируем форму текущим объектом конференции.
        form = ConferenceForm(instance=conference)

    # Формируем контекст для передачи данных на страницу.
    context = {
        'form': form
    }
    # Рендерим страницу с переданным контекстом.
    return render(request, 'edit_conference.html', context)

# Страница удаления конференции.
@login_required
def delete_conference(request, conference_id):
    # Получаем объект конференции или возвращаем 404 ошибку, если такого объекта нет.
    conference = get_object_or_404(Conference, id=conference_id)

    # Проверяем, является ли текущий пользователь автором конференции.
    if request.user != conference.author:
        # Если пользователь не автор, возвращаем ошибку 403.
        return HttpResponseForbidden("You don't have permission to delete this conference.")

    # Проверяем, является ли запрос POST-запросом.
    if request.method == 'POST':
        # Удаляем конференцию.
        conference.delete()
        # Перенаправляем пользователя на главную страницу.
        return redirect('home')

    # Формируем контекст для передачи данных на страницу.
    context = {
        'conference': conference
    }
    # Рендерим страницу с переданным контекстом.
    return render(request, 'delete_conference.html', context)

# Страница деталей конференции.
@login_required
def conference_detail(request, conference_id):
    # Получаем объект конференции или возвращаем 404 ошибку, если такого объекта нет.
    conference = get_object_or_404(Conference, id=conference_id)
    # Получаем список регистраций для данной конференции.
    registrations = Registration.objects.filter(conference=conference)
    # Получаем список отзывов для данной конференции.
    reviews = Review.objects.filter(conference=conference)

    # Формируем контекст для передачи данных на страницу.
    context = {
        'conference': conference,
        'registrations': registrations,
        'reviews': reviews
    }
    # Рендерим страницу с переданным контекстом.
    return render(request, 'conference_detail.html', context)

# Страница добавления отзыва к конференции.
@login_required
def add_review(request, conference_id):
    # Получаем объект конференции или возвращаем 404 ошибку, если такого объекта нет.
    conference = get_object_or_404(Conference, id=conference_id)

    # Проверяем, является ли запрос POST-запросом.
    if request.method == 'POST':
        # Инициализируем форму данными из запроса.
        form = ReviewForm(request.POST)
        # Проверяем валидность данных формы.
        if form.is_valid():
            # Сохраняем данные формы в объект, но ещё не коммитим в базу данных.
            review = form.save(commit=False)
            # Устанавливаем конференцию и пользователя для отзыва.
            review.conference = conference
            review.user = request.user
            # Сохраняем отзыв в базу данных.
            review.save()
            # Перенаправляем пользователя на страницу деталей конференции.
            return redirect('conference_detail', conference_id=conference_id)
    else:
        # Если запрос не POST, инициализируем пустую форму.
        form = ReviewForm()

    # Формируем контекст для передачи данных на страницу.
    context = {'form': form, 'conference': conference}
    # Рендерим страницу с переданным контекстом.
    return render(request, 'review_form.html', context)

# Страница регистрации на конференцию.
@login_required
def register_for_conference(request, conference_id):
    # Получаем объект конференции или возвращаем 404 ошибку, если такого объекта нет.
    conference = get_object_or_404(Conference, id=conference_id)

    # Проверяем, является ли запрос POST-запросом.
    if request.method == 'POST':
        # Инициализируем форму данными из запроса.
        form = RegistrationForm(request.POST)
        # Проверяем валидность данных формы.
        if form.is_valid():
            # Сохраняем данные формы в объект, но ещё не коммитим в базу данных.
            registration = form.save(commit=False)
            # Устанавливаем конференцию и пользователя для регистрации.
            registration.conference = conference
            registration.user = request.user
            # Сохраняем регистрацию в базу данных.
            registration.save()
            # Перенаправляем пользователя на страницу деталей конференции.
            return redirect('conference_detail', conference_id=conference_id)
    else:
        # Если запрос не POST, инициализируем пустую форму.
        form = RegistrationForm()

    # Формируем контекст для передачи данных на страницу.
    context = {'form': form, 'conference': conference}
    # Рендерим страницу с переданным контекстом.
    return render(request, 'registration_form.html', context)

