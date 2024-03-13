from rest_framework import routers
from . import views

router = routers.SimpleRouter()

router.register('conferences', viewset=views.ConfrenceViewSet)
router.register('topics', viewset=views.TopicViewSet)
router.register('reviews', viewset=views.ReviewViewSet)
router.register('registrations', viewset=views.RegistrationViewSet)
router.register('profile', viewset=views.ProfileViewSet)

urlpatterns = router.urls
