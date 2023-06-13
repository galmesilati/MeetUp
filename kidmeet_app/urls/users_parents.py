from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kidmeet_app.views.users_parents import ParentsViewSet

router = DefaultRouter()
router.register('', ParentsViewSet)

urlpatterns = [
    path('parents/', include(router.urls))
]

# adding parents urls to urlpatterns
urlpatterns.extend(router.urls)