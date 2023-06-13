from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


# Create your views here.

# @api_view(['GET'])
# def get_children(request: Request):
#     all_children = Child.objects.all()
#     print("initial query:", data=all_children.query)


@api_view(['POST'])
def signup(request):
    pass





