from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kidmeet_app.models import Child, Event, ChildEvent, Interests, ChildInterests, Schedule
from kidmeet_app.serializers.children import ChildSerializer, InterestsSerializer, ScheduleSerializer, EventSerializer
from kidmeet_app.views.filters import ChildFilterSet, EventFilterSet, ScheduleFilterSet


class ChildViewSet(ModelViewSet):
    serializer_class = ChildSerializer
    queryset = Child.objects.all()
    filterset_class = ChildFilterSet
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        child_data = request.data.copy()
        child_data['user'] = request.user.id

        serializer = self.get_serializer(data=child_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,headers=headers)

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

    @action(detail=False, methods=['POST'])
    def create_event(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def child_events(self, request):

        title_to_search = request.GET.get('title')

        user = request.user
        children = Child.objects.filter(user=user)
        child_events = Event.objects.filter(childevent__child__in=children)
        if title_to_search:
            child_events = child_events.filter(title=title_to_search)

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

    @action(detail=True, methods=['GET'])
    def child_schedule(self, request, pk=None):
        user = request.user
        children = Child.objects.filter(user=user)
        ser = ChildSerializer(children, many=True)
        return Response(data=ser.data)

    @action(detail=True, methods=['GET'])
    def view_child_schedule(self, request, pk=None):
        child_id = pk
        schedule_data = Schedule.objects.filter(child_id=child_id)
        serializer = ScheduleSerializer(schedule_data, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def set_regular_activities(self, request, pk=None):
        print('Gal request', request)
        child_id = request.data.get('child_id')
        schedule_data = request.data.get('schedule_data', [])
        update_type = request.data.get('update_type', 'following_weeks')
        child = Child.objects.get(pk=child_id)

        print('child', child)

        for day in schedule_data:
            start_datetime = datetime.strptime(day.get('start_time'), "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.strptime(day.get('end_time'), "%Y-%m-%d %H:%M:%S")

            print('start_time:', start_datetime)
            print('end_time', end_datetime)

            type_activity = day.get('type_activity')
            print('activity', type_activity)

            current_time = start_datetime

            while current_time <= end_datetime:
                day_of_week = current_time.strftime('%A').lower()

                schedule_data = {
                    'child': child,
                    'start_time': current_time,
                    'end_time': current_time + timedelta(hours=(end_datetime - start_datetime).seconds // 3600),
                    'type_activity': type_activity,
                    'day_of_week': day_of_week
                }
                Schedule.objects.create(**schedule_data)

                current_time += timedelta(weeks=1)

            if update_type == 'current_week':
                break

        return Response({'message': 'Schedule updated successfully'}, status=status.HTTP_200_OK)






















