'''
Filename:views.py
Time:2023/6/18
Author: Fshrimp
Describe:
'''
import json

from django.shortcuts import render
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from api.infomanage.models import App_Info as Ai
from api.infomanage.models import App_rapid_reduction as Arr
from api.infomanage.models import App_rapid_expansion as Are


# 封装返回结果
def get_message(status, msg, **kwargs):
    if kwargs:
        for k, v in kwargs.items():
            result = {"code": status, "message": msg, k: v}
    else:
        result = {"code": status, "message": msg}
    return result


# 判断字典里的所有的value是否都为某个值
def all_values_equal_to(dictionary, target_value):
    num = 0
    for key, value in dictionary.items():
        if key not in ["aid", "appname", "on_special_content", "off_special_content"]:
            if value != target_value:
                num += 1
        if key == "on_special_content" or key == "off_special_content":
            if value != "":
                if value != "None":
                    num += 1
    return True if num == 0 else False


# 展示系统的基础信息
def show_info(request):
    apif_dict, items_li = dict(), list()
    if request.method == 'GET':
        # 获取请求参数
        data = request.GET
        if data.get("flag") is None:
            result = get_message('404', "missing parameter：flag")
            return JsonResponse(result)
        else:
            total = len(Ai.objects.filter().all())
            appname = data.get("appname")
            # 若flag为1，则表示模糊过滤系统名
            if int(data.get("flag")) == 1:
                page_data = Ai.objects.filter(appname__icontains=appname).all()
            # flag为0表示过滤所有信息
            else:
                pagesize = int(data.get("limit"))
                page = int(data.get("page"))  # encRow
                app_info = Ai.objects.all()
                app_obj = Paginator(app_info, pagesize)
                page_data = app_obj.get_page(page)
        for ap_i in page_data:
            aid, appname = ap_i.aid, ap_i.appname
            # 业务域和系统负责人
            app_domain, app_Owner = ap_i.app_domain, ap_i.app_Owner
            # 可随时重启
            judge_info_restart = make_rapid_data(appname, "restart")["data"]
            # 判断
            restart_any = "是" if all_values_equal_to(judge_info_restart, "是") else "否"
            # 可快速扩容
            judge_info_ex = make_rapid_data(appname, "true")["data"]
            rapid_expansion = "是" if all_values_equal_to(judge_info_ex, "是") else "否"
            # 可快速缩容
            judge_info_re = make_rapid_data(appname, "false")["data"]
            rapid_reduction = "是" if all_values_equal_to(judge_info_re, "是") else "否"
            # 组合数据返回的数据
            judge_info = make_rapid_data(appname, "other")["data"]
            judge_info["aid"], judge_info["appname"], judge_info["app_domain"], judge_info["app_Owner"], \
                judge_info["restart_any"], judge_info["rapid_reduction"], judge_info["rapid_expansion"], \
                = aid, appname, app_domain, app_Owner, restart_any, rapid_reduction, rapid_expansion
            items_li.append(judge_info)
        result = get_message(20000, "get app info success", data=items_li)
    else:
        result = get_message(500, "get app info failed: request not get mothod")
    result["total"] = total
    return JsonResponse(result)


# 展示系统的快速扩缩容信息
def show_rapid_info(request):
    if request.method == 'GET':
        # 获取请求参数
        data = request.GET
        # 判断是否缺少参数
        if data.get("appname") is None:
            result = get_message(404, "missing parameter：appname")
        elif data.get("rrflag") is None:
            result = get_message(404, "missing parameter：rrflag")
        else:
            appname = data.get("appname")
            flag = data.get("rrflag")
            result = make_rapid_data(appname, flag)
    else:
        result = get_message(500, "get app rapid info failed: request not get mothod")
    return JsonResponse(result)


def make_rapid_data(appname, flag):
    info_tmp_reatsrt = dict()
    # 查询数据库（快速扩容和快速缩容）
    app_rapidex = Are.objects.filter(appname=appname)
    app_rapidre = Arr.objects.filter(appname=appname)
    # 遍历快速扩容result
    for ex_info in app_rapidex:
        info_tmp_ex = dict()
        aid, appname = ex_info.aid, ex_info.appname
        # 支持一键扩容初始化
        once_init = ex_info.once_init
        # 支持deploy.sh部署
        on_deploy = ex_info.on_deploy
        # 可随时启动服务
        start_any = ex_info.start_any
        # 支持健康检查判断服务状态
        health_check = ex_info.health_check
        # 可随时上流量
        online_any = ex_info.online_any
        # 特殊项描述
        on_special_content = ex_info.on_special_content
        info_tmp_ex["aid"], info_tmp_ex["appname"], info_tmp_ex["once_init"], info_tmp_ex["on_deploy"], \
            info_tmp_ex["start_any"], info_tmp_ex["online_any"], info_tmp_ex["health_check"], info_tmp_ex[
            "on_special_content"] \
            = aid, appname, once_init, on_deploy, start_any, health_check, online_any, on_special_content
    # 遍历快速缩容result
    for re_info in app_rapidre:
        info_tmp_re = dict()
        aid, appname = re_info.aid, re_info.appname
        # 可随时下流量
        offline_any = re_info.offline_any
        # 可随时停止服务
        stop_any = re_info.stop_any
        # 支持日志备份
        logback = re_info.logback
        # 特殊项描述
        off_special_content = re_info.off_special_content
        info_tmp_re["aid"], info_tmp_re["appname"], info_tmp_re["offline_any"], info_tmp_re["stop_any"], \
            info_tmp_re["logback"], info_tmp_re[
            "off_special_content"] = aid, appname, offline_any, stop_any, logback, off_special_content
    info_tmp_reatsrt["offline_any"], info_tmp_reatsrt["stop_any"], info_tmp_reatsrt["start_any"], info_tmp_reatsrt[
        "online_any"] \
        = offline_any, stop_any, start_any, online_any
    # 判断flag的值
    # 为true表示获取快速扩容的数据
    if flag == "true":
        result = get_message(20000, "get app rapid info success", data=info_tmp_ex)
    # 为false表示获取快速缩容的数据
    elif flag == "false":
        result = get_message(20000, "get app rapid info success", data=info_tmp_re)
    elif flag == "restart":
        result = get_message(20000, "get app rapid info success", data=info_tmp_reatsrt)
    # 为other表示获取组合信息
    elif flag == "other":
        make_info_tmp = {**info_tmp_re, **info_tmp_ex}
        result = get_message(20000, "get app rapid info success", data=make_info_tmp)
    return result

#更新数据
def update_info(request):
    all_dict, re_dict, ex_dict = dict(), dict(), dict()
    if request.method == 'GET':
        # 获取请求参数
        data = request.GET
        # 判断是否缺少参数
        if data.get("appname") is None:
            result = get_message(404, "missing parameter：appname")
        else:
            try:
                ex_dict["appname"], ex_dict["once_init"], ex_dict["on_deploy"], ex_dict["start_any"], \
                    ex_dict["health_check"], ex_dict["online_any"], ex_dict["on_special_content"] \
                    = data.get("appname"), data.get("once_init"), data.get("on_deploy"), data.get("start_any"), \
                    data.get("health_check"), data.get("online_any"), data.get("on_special_content")
                re_dict["appname"], re_dict["offline_any"], re_dict["stop_any"], re_dict["logback"], re_dict[
                    "off_special_content"] \
                    = data.get("appname"), data.get("offline_any"), \
                    data.get("stop_any"), data.get("logback"), data.get("off_special_content")
                all_dict["appname"], all_dict["app_domain"], all_dict["app_Owner"] \
                    = data.get("appname"), data.get("app_domain"), data.get("app_Owner")
                all_dict["rapid_expansion"] = "是" if all_values_equal_to(ex_dict, "是") else "否"
                all_dict["rapid_reduction"] = "是" if all_values_equal_to(re_dict, "是") else "否"
                if ex_dict["start_any"] == "是" and ex_dict["online_any"] == "是" and re_dict["stop_any"] == "是" and \
                        re_dict["offline_any"] == "是":
                    all_dict["restart_any"] = "是"
                else:
                    all_dict["restart_any"] = "否"
                Ai.objects.filter(appname=data.get("appname")).update(**all_dict)
                Arr.objects.filter(appname=data.get("appname")).update(**re_dict)
                Are.objects.filter(appname=data.get("appname")).update(**ex_dict)
                result = get_message(20000, "update info success")
            except Exception as e:
                result = get_message(500, "update info failed", data=e)
    else:
        result = get_message(500, "update info failed: request not get mothod")
    return JsonResponse(result)

#插入数据
def insert_info(request):
    all_dict, re_dict, ex_dict = dict(), dict(), dict()
    if request.method == 'GET':
        # 获取请求参数
        data = request.GET
        try:
            ex_dict["appname"], ex_dict["once_init"], ex_dict["on_deploy"], ex_dict["start_any"], \
                ex_dict["health_check"], ex_dict["online_any"], ex_dict["on_special_content"] \
                = data.get("appname"), data.get("once_init"), data.get("on_deploy"), data.get("start_any"), \
                data.get("health_check"), data.get("online_any"), data.get("on_special_content")
            re_dict["appname"], re_dict["offline_any"], re_dict["stop_any"], re_dict["logback"], re_dict[
                "off_special_content"] \
                = data.get("appname"), data.get("offline_any"), \
                data.get("stop_any"), data.get("logback"), data.get("off_special_content")
            all_dict["appname"], all_dict["app_domain"], all_dict["app_Owner"] \
                = data.get("appname"), data.get("app_domain"), data.get("app_Owner")
            all_dict["rapid_expansion"] = "是" if all_values_equal_to(ex_dict, "是") else "否"
            all_dict["rapid_reduction"] = "是" if all_values_equal_to(re_dict, "是") else "否"
            if ex_dict["start_any"] == "是" and ex_dict["online_any"] == "是" and re_dict["stop_any"] == "是" and \
                    re_dict["offline_any"] == "是":
                all_dict["restart_any"] = "是"
            else:
                all_dict["restart_any"] = "否"
            ai = Ai(**all_dict)
            arr = Arr(**re_dict)
            are = Are(**ex_dict)
            ai.save(),arr.save(),are.save()
            result = get_message(20000, "insert info success")
        except Exception as e:
            result = get_message(500, "insert info failed", data=e)
    else:
        result = get_message(500, "insert info failed: request not get mothod")
    return JsonResponse(result)

#删除数据
def delete_info(request):
    if request.method == 'GET':
        # 获取请求参数
        data = request.GET
        try:
            # 判断是否缺少参数
            if data.get("appname") is None:
                result = get_message(404, "missing parameter：appname")
            else:
                appname = data.get("appname")
                del_data_ai = Ai.objects.get(appname=appname)
                del_data_arr = Arr.objects.get(appname=appname)
                del_data_are = Are.objects.get(appname=appname)
                del_data_ai.delete(),del_data_arr.delete(),del_data_are.delete()
                result = get_message(20000, "delete info success")
        except Exception as e:
            result = get_message(500, "delete info failed", data=e)
    else:
        result = get_message(500, "delete info failed: request not get mothod")
    return JsonResponse(result)