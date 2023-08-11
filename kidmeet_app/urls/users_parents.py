from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kidmeet_app.views.users_parents import UserViewSet

router = DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    # path('parents/', include(router.urls))
]

# adding parents urls to urlpatterns
urlpatterns.extend(router.urls)