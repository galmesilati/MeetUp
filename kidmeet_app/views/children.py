from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kidmeet_app.models import Child, Event
from kidmeet_app.serializers.children import ChildSerializer, DetailedEventChildSerializer


@api_view(['GET'])
def get_children(request):
    all_children = Child.objects.all()
    serializer = ChildSerializer(instance=all_children, many=True)
    return Response(data= serializer.data)


class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        name = request.query_params.get('name')
        age = request.query_params.get('age')

        if name:
            queryset = queryset.filter(name__iexact=name)
        if age:
            queryset = queryset.filter(age=age)

        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)


@api_view(['GET'])
def get_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    serializer = ChildSerializer(instance=child)
    return Response(data=serializer.data)


class EventViewSet(ModelViewSet):
    serializer_class = DetailedEventChildSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        queryset = Event.objects.all()
        title = self.request.query_params.get('title')
        description = self.request.query_params.get('description')
        start_event = self.request.query_params.get('start_event')
        end_event = self.request.query_params.get('end_event')
        location = self.request.query_params.get('location')

        if title:
            queryset = queryset.filter(title__iexact='title').values()
        if description:
            queryset = queryset.filter(description__iexact='description').values()
        if start_event:
            queryset = queryset.filter(start_event__gte__iexact='start_event').values()
        if end_event:
            queryset = queryset.filter(end_event__lte__iexact='end_event').values()
        if location:
            queryset = queryset.filter(location__iexact='location').values()

        return queryset
        # return queryset.prefetch_related('childevent_set__child')

    def create_new_event(self, request):
        child_id = request.data.get('child_id')
        title = request.data.get('title')
        description = request.data.get('description')
        start_event = request.data.get('start_event')
        end_event = request.data.get('end_event')
        location = request.data.get('location')
        try:
            event = Event.objects.get(id=child_id)
        except Child.DoesNotExist:
            return Response({'error': f'Child with id {child_id} does not exist'})

        event = Event(title=title, description=description,start_event=start_event,end_event=end_event,location=location)
        event.save()
        serializer = DetailedEventChildSerializer(event)

        return Response(data=serializer.data)


@api_view(['GET'])
def get_events(request):
    all_events = Event.objects.all()
    serializer = DetailedEventChildSerializer(instance=all_events, many=True)
    return Response(data=serializer.data)


@api_view(['PUT', 'PATCH', 'DELETE'])
def get_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method in ('PUT', 'PATCH'):
        serializer = DetailedEventChildSerializer(instance=event,
                                                  data=request.data,
                                                  partial=request.method == 'PATCH'
                                                  )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
    else:
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_events_for_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    events = child.childevent_set.values('event')
    event_ids = [event['event'] for event in events]
    events = Event.objects.filter(id__in=event_ids)
    return events


@api_view(['GET'])
def get_children_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    children = event.childevent_set.values('child')
    child_ids = [child['child'] for child in children]
    children = Child.objects.filter(id__in=child_ids)
    return children











