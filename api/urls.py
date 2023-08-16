# -*- coding:UTF-8 -*-
'''
Filename:urls.py
Time:2023/8/11 
Author: Fshrimp
Describe:配置api的路由
'''

from django.urls import path,include
import api.testapi.urls
import api.infomanage.urls

urlpatterns = [
    path('tp/', include(api.testapi.urls)),
    path('mana_info/',include(api.infomanage.urls)),
]