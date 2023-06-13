from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from kidmeet_app.models import Child
from kidmeet_app.serializers.children import ChildSerializer


# @api_view(['GET'])
# def get_children(request):
#     all_children = Child.objects.all()
#     serializer = ChildSerializer(instance=all_children, many=True)
#     return Response(data= serializer.data)

class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]

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


