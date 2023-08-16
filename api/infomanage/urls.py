# -*- coding:UTF-8 -*-
'''
Filename:urls.py
Time:2023/8/11 
Author: Fshrimp
Describe:系统信息管理功能路由配置
'''

from django.contrib import admin
from django.urls import path
from api.infomanage import views

urlpatterns = [
    path('show_info/', views.show_info),
    path('show_rdinfo/',views.show_rapid_info),
    path('update_info/',views.update_info),
    path('insert_info/',views.insert_info),
    path('delete_info/',views.delete_info),
]