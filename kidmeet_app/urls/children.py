from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kidmeet_app.views.children import get_children, get_child, get_event, get_events, create_new_event, \
    create_new_interests, get_all_interests, interests_child_handler, create_child_schedule, create_new_child, \
    get_available_children

router = DefaultRouter()
# router.register('', ChildViewSet)

urlpatterns = [
    # path('children/', include(router.urls))
    path('children/', get_children),
    path('child/<int:child_id>/', get_child),
    path('event/<int:event_id>', get_event),
    path('events/', get_events),
    path('new_event', create_new_event),
    path('new_interest', create_new_interests),
    path('all_interests', get_all_interests),
    path('interests_child', interests_child_handler),
    path('new_schedule', create_child_schedule),
    path('create_child', create_new_child),
    path('available-child', get_available_children)
]




urlpatterns.extend(router.urls)