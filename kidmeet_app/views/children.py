from datetime import datetime

import django_filters
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kidmeet_app.models import Child, Event, ChildEvent, Interests, ChildInterests, Schedule
from kidmeet_app.serializers.children import ChildSerializer, InterestsSerializer, ScheduleSerializer, EventSerializer
from kidmeet_app.views.filters import ChildFilterSet, EventFilterSet, ScheduleFilterSet


# @api_view(['POST'])
# def create_child_schedule(request):
#     new_schedule = ScheduleSerializer(data=request.data)
#     new_schedule.is_valid(raise_exception=True)
#     new_schedule.save()
#     return Response(status=status.HTTP_201_CREATED, data=new_schedule.data)


# @api_view(['POST'])
# def create_new_interests(request):
#     name = request.data.get('name')
#     interests = Interests(name=name)
#     interests.save()
#     serializer = InterestsSerializer(interests)
#
#     return Response(status=status.HTTP_201_CREATED, data=request.data)
#
#
# @api_view(['GET'])
# def get_all_interests(request):
#     interests = Interests.objects.all()
#     serializer = InterestsSerializer(instance=interests, many=True)
#     return Response(data=serializer.data)


# @api_view(['POST', 'PATCH', 'DELETE'])
# def interests_child_handler(request):
#     interest_id = request.POST.get('interest_id')
#     child_id = request.POST.get('child_id')
#     if request.method == 'POST' and interest_id and child_id:
#         interest = get_object_or_404(Interests, interest_id=interest_id)
#         child_interests = ChildInterests(child_id=child_id, interest_id=interest_id)
#         child_interests.save()
#         return Response(status=status.HTTP_201_CREATED)


class ChildViewSet(ModelViewSet):
    serializer_class = ChildSerializer
    queryset = Child.objects.all()
    filterset_class = ChildFilterSet
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        return super(ChildViewSet, self).create(request, *args, **kwargs)

    @action(detail=False)
    def user_children(self, request):
        print(request)
        user = request.user
        children = Child.objects.filter(user=user)
        ser = ChildSerializer(children, many=True)
        return Response(data=ser.data)

    def get_available_children(self):
        pass


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filterset_class = EventFilterSet

    @action(detail=False)
    def child_events(self, request):
        user = request.user
        children = Child.objects.filter(user=user)
        child_events = Event.objects.filter(childevent__child__in=children)
        ser = EventSerializer(child_events, many=True)
        return Response(data=ser.data)


@api_view(['GET'])
def get_title_events(request):
    all_title = list(Event.objects.order_by().values_list('title').distinct())
    all_title = [title for sublist in all_title for title in sublist]
    print(all_title)
    return JsonResponse(data=list(all_title), safe=False)


class InterestViewSet(ModelViewSet):
    queryset = Interests.objects.all()
    serializer_class = InterestsSerializer

    @action(detail=False, methods=['POST'])
    def create_interests_child_handler(self, request):
        data = request.data
        serializer = InterestsSerializer(data=data)

        if serializer.is_valid():
            interest = serializer.save()
            return Response({f"Interest {interest.name} created and linked to child successfully!"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filterset_class = ScheduleFilterSet

    def child_schedule(self, request):
        user = request.user
        children = Child.objects.filter(user=user)
        ser = ChildSerializer(children, many=True)
        return Response(data=ser.data)












