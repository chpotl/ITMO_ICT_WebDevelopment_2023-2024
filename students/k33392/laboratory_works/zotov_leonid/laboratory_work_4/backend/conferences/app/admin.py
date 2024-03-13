from django.contrib import admin
from .models import Conference, Topic, Registration, Review

admin.site.register(Conference)
admin.site.register(Topic)
admin.site.register(Registration)
admin.site.register(Review)