from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kidmeet_app.views.children import \
    create_new_interests, get_all_interests, create_child_schedule, \
    ChildViewSet, EventViewSet, InterestViewSet

router = DefaultRouter()
router.register('children', ChildViewSet)

router.register('event', EventViewSet)


router.register('interest', InterestViewSet)

urlpatterns = router.urls

# urlpatterns = [
    # path('children/', include(router.urls))
    # path('children/', get_children),
    # path('child/<int:child_id>/', get_child),
    # path('event/<int:event_id>', get_event),
    # path('events/', get_events),
    # path('new_event', create_new_event),
    # path('new_interest', create_new_interests),
    # path('all_interests', get_all_interests),
    # path('interests_child', interests_child_handler),
    # path('new_schedule', create_child_schedule),
    # path('create_child', create_new_child),
    # path('available-child', ChildFilterSet)
# ]


# urlpatterns.extend(router.urls)