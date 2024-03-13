"""
URL configuration for laboratory_work_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from list_of_conferences import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('create-conference/', views.create_conference, name='create_conference'),
    path('edit_conference/<int:conference_id>/', views.edit_conference, name='edit_conference'),
    path('delete_conference/<int:conference_id>/', views.delete_conference, name='delete_conference'),
    path('conference/<int:conference_id>/', views.conference_detail, name='conference_detail'),
    path('conference/<int:conference_id>/review/', views.add_review, name='add_review'),
    path('conference/<int:conference_id>/register/', views.register_for_conference, name='register_for_conference'),
]
