from datetime import datetime

import django_filters
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kidmeet_app.models import Child, Event, ChildEvent, Interests, ChildInterests, Schedule
from kidmeet_app.serializers.children import ChildSerializer, InterestsSerializer, \
    ChildInterestsSerializer, ScheduleSerializer, AvailableChildSerializer, EventSerializer
from kidmeet_app.views.filters import ChildFilterSet, EventFilterSet


@api_view(['GET'])
def get_children(request):
    all_children = Child.objects.all()
    serializer = ChildSerializer(instance=all_children, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_child(request, child_id):
    child = get_object_or_404(Child, child_id=child_id)
    serializer = ChildSerializer(instance=child)
    return Response(data=serializer.data)


@api_view(['POST'])
def create_new_child(request):
    new_child = ChildSerializer(data=request.data)
    new_child.is_valid(raise_exception=True)
    new_child.save()
    return Response(status=status.HTTP_201_CREATED, data=new_child.data)


@api_view(['POST'])
def create_new_event(request):
    child_id = request.data.get('child_id')
    title = request.data.get('title')
    description = request.data.get('description')
    start_event = request.data.get('start_event')
    end_event = request.data.get('end_event')
    location = request.data.get('location')
    try:
        child = Child.objects.get(child_id=child_id)
    except Child.DoesNotExist:
        return Response({'error': f'Child with id {child_id} does not exist'})

    event = Event(title=title, description=description, start_event=start_event, end_event=end_event, location=location)
    event.save()
    serializer = DetailedEventChildSerializer(event)
    child_event = ChildEvent(child_id=child_id, event_id=event.event_id)
    child_event.save()

    return Response(data=serializer.data)


@api_view(['POST'])
def create_child_schedule(request):
    new_schedule = ScheduleSerializer(data=request.data)
    new_schedule.is_valid(raise_exception=True)
    new_schedule.save()
    return Response(status=status.HTTP_201_CREATED, data=new_schedule.data)


@api_view(['POST'])
def create_new_interests(request):
    name = request.data.get('name')
    interests = Interests(name=name)
    interests.save()
    serializer = InterestsSerializer(interests)

    return Response(status=status.HTTP_201_CREATED, data=request.data)


@api_view(['GET'])
def get_all_interests(request):
    interests = Interests.objects.all()
    serializer = InterestsSerializer(instance=interests, many=True)
    return Response(data=serializer.data)


@api_view(['POST', 'PATCH', 'DELETE'])
def interests_child_handler(request):
    interest_id = request.POST.get('interest_id')
    child_id = request.POST.get('child_id')
    if request.method == 'POST' and interest_id and child_id:
        interest = get_object_or_404(Interests, interest_id=interest_id)
        child_interests = ChildInterests(child_id=child_id, interest_id=interest_id)
        child_interests.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_events(request):
    all_events = Event.objects.all()
    serializer = DetailedEventChildSerializer(instance=all_events, many=True)
    return Response(data=serializer.data)


@api_view(['GET', 'PATCH', 'DELETE'])
def get_event(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    if request.method == 'GET':
        serializer = DetailedEventChildSerializer(event)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    elif request.method == 'PATCH':
        serializer = DetailedEventChildSerializer(instance=event,
                                                  data=request.data,
                                                  partial=True
                                                  )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
    else:
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChildViewSet(ModelViewSet):
    serializer_class = ChildSerializer
    queryset = Child.objects.all()
    filterset_class = ChildFilterSet


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filterset_class = EventFilterSet






