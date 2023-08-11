import django_filters
from django.db.models import Q

from kidmeet_app.models import Child, Event


class ChildFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    age = django_filters.NumberFilter(lookup_expr='exact')
    study_framework = django_filters.CharFilter(method='study_filter')
    event_title = django_filters.CharFilter(field_name='events__title', lookup_expr='exact')
    interest_name = django_filters.CharFilter(field_name='interests__name', lookup_expr='exact')


    def study_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(kindergarten__iexact=value) |
                                   Q(school__iexact=value) |
                                   Q(classroom__icontains=value))
        return queryset

    class Meta:
        model = Child
        fields = ['name', 'age', 'study_framework', 'event_title', 'interest_name']


class EventFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')

    date_only = django_filters.DateFilter(field_name='start_event', lookup_expr='date')
    start_event_range = django_filters.DateFromToRangeFilter(field_name='start_event')

    def filter_start_event_range(self, queryset, name, value):
        if value.start:
            queryset = queryset.filter(start_event__gte=value.start)
        if value.stop:
            queryset = queryset.filter(start_event_lt=value.stop)
        return queryset

    class Meta:
        model = Event
        fields = []
