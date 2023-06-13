from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kidmeet_app.views.children import ChildViewSet

router = DefaultRouter()
router.register('', ChildViewSet)

urlpatterns = [
    path('child/', include(router.urls))
]


urlpatterns.extend(router.urls)