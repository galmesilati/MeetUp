from django.urls import path, include
from rest_framework.routers import DefaultRouter


from kidmeet_app.views.users_parents import UserViewSet, upload_profile_img

router = DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    # path('parents/', include(router.urls))
    path('profile/img', upload_profile_img)
]

# adding parents urls to urlpatterns
urlpatterns.extend(router.urls)