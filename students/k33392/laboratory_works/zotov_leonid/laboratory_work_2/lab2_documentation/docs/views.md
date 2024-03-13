# Представления

# index

## Код

`def index(request):
    conferences = Conference.objects.all()
    participants_per_conference = {}
    for conf in conferences:
        participants = Registration.objects.filter(conference=conf)
        participants_per_conference[conf] = participants
    return render(request, 'index.html', {
        'conferences': conferences,
        'participants_per_conference': participants_per_conference
    })`

## Описание

Главная страница сайта, отображающая все доступные конференции и количество участников в каждой из них.

## URL-шаблон: /

# register

## Код

`def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}! Теперь вы можете войти в систему.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})`

## Описание

Страница регистрации нового пользователя.

## URL-шаблон: /register/

# user_login

## Код

`def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')
    return render(request, 'registration/login.html')`

## Описание

Страница входа в систему.

## URL-шаблон: /login/

# home

## Код

`def home(request):
    user_conferences = Conference.objects.filter(author=request.user)
    other_conferences = Conference.objects.exclude(author=request.user) 
    context = {
        'user_conferences': user_conferences,
        'other_conferences': other_conferences,
    }
    return render(request, 'home.html', context)`

## Описание

Главная страница для авторизованного пользователя, отображающая созданные им конференции и другие доступные конференции.

## URL-шаблон: /home/

# create_conference

## Код

`def create_conference(request):
    if request.method == 'POST':
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save(commit=False)
            conference.author = request.user
            conference.save()
            return redirect('home')
    else:
        form = ConferenceForm()
    context = {
        'form': form
    }
    return render(request, 'create_conference.html', context)`

## Описание

Страница создания новой конференции.

## URL-шаблон: /create_conference/

# edit_conference

## Код

`def edit_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.user != conference.author:
        return HttpResponseForbidden("You don't have permission to edit this conference.")
    if request.method == 'POST':
        form = ConferenceForm(request.POST, instance=conference)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ConferenceForm(instance=conference)
    context = {
        'form': form
    }
    return render(request, 'edit_conference.html', context)`

## Описание

Страница редактирования конференции.

## URL-шаблон: /edit_conference/<int:conference_id>/

# delete_conference

## Код

`def delete_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.user != conference.author:
    return HttpResponseForbidden("You don't have permission to delete this conference.")
    if request.method == 'POST':
        conference.delete()
        return redirect('home')
    context = {
    'conference': conference
    }
    return render(request, 'delete_conference.html', context)`

## Описание

Страница удаления конференции.

## URL-шаблон: /delete_conference/<int:conference_id>/

# conference_detail

## Код

`def conference_detail(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    registrations = Registration.objects.filter(conference=conference)
    reviews = Review.objects.filter(conference=conference)
    context = {
        'conference': conference,
        'registrations': registrations,
        'reviews': reviews
    }
    return render(request, 'conference_detail.html', context)`

## Описание

Страница детального просмотра конференции, включая список участников и отзывы.

## URL-шаблон: /conference/<int:conference_id>/

# add_review

## Код

`def add_review(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.conference = conference
        review.user = request.user
        review.save()
        return redirect('conference_detail', conference_id=conference_id)
    else:
        form = ReviewForm()
    context = {'form': form, 'conference': conference}
    return render(request, 'review_form.html', context)`

## Описание

Страница добавления отзыва о конференции.

## URL-шаблон: /add_review/<int:conference_id>/

# register_for_conference

`def register_for_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.conference = conference
            registration.user = request.user
            registration.save()
            return redirect('conference_detail', conference_id=conference_id)
    else:
        form = RegistrationForm()
    context = {'form': form, 'conference': conference}
    return render(request, 'registration_form.html', context)`

## Описание

Страница регистрации на конференцию.

## URL-шаблон: /register_for_conference/<int:conference_id>/
