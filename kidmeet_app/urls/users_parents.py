from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kidmeet_app.views.users_parents import get_all_parents

router = DefaultRouter()
# router.register('', ParentsViewSet)

urlpatterns = [
    # path('parents/', include(router.urls))
    path('parents/', get_all_parents)
]

# adding parents urls to urlpatterns
urlpatterns.extend(router.urls)