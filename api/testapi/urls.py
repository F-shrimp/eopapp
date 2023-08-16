# -*- coding:UTF-8 -*-
'''
Filename:urls.py
Time:2023/8/11 
Author: Fshrimp
Describe:testapi 路由
'''
from django.contrib import admin
from django.urls import path,include
from api.testapi import views

urlpatterns = [
    path('a/', views.index),
]