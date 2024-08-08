from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
import requests
import json
from myapp.models import User


def test(request):
    users = serializers.serialize("json", User.objects.all())
    return JsonResponse({"status": 0, "users": users})
