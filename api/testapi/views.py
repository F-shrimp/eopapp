from django.shortcuts import render
from django.http.response import  JsonResponse
from sqlalchemy import or_
from rest_framework.parsers import JSONParser
from api.testapi.models import App_Info1 as Ai

#测试请求数据库
def index(request):
    if request.method in ['GET','POST']:
        api_info = Ai.objects.filter().all()
        print(api_info)
        return JsonResponse({"status": 200})
    return JsonResponse({"status": 200})

# Create your views here.
