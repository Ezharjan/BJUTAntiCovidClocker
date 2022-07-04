#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import time
import datetime
import pickle
import requests
import random


def notification(param, key="", action="changed"):
    # Define your own notification.
    # Get notification of warnings and status
    # If return False, then stop the submit process
    return True


if __name__ == "__main__":

    # 填写用户名和密码
    username = "20080205"
    password = "123456789"

    location = ""

    if location == "":
        print("【生成地址】没有指定地址，正在生成随机地址…")
        # lng = 116.397499 + random.random() / 10.0 - 0.05
        # lat = 39.908722 + random.random() / 10.0 - 0.05
        # 学校
        lng = 116.473056
        lat = 39.877778
        # 广东茂名——经纬度随便改，但不要超出我国，否则会为空
        # lng = 111
        # lat = 22
        coordination = str(lng) + "," + str(lat)
        PARAMS = {
            "key": "729923f88542d91590470f613adb27b5",
            "s": "rsv3",
            "location": coordination,
        }
        r = requests.get(url="https://restapi.amap.com/v3/geocode/regeo", params=PARAMS)
        location = r.json()
        location["lng"] = lng
        location["lat"] = lat
        try:
            print(r.json()["regeocode"]["formatted_address"])
            print("3 秒钟后继续")
            time.sleep(3)
        except:
            print("生成地址时遇到问题")
            exit("程序已经中断")
    else:
        location = json.loads(location)
        lng = location["lng"]
        lat = location["lat"]
        print("【使用地址】" + location["regeocode"]["formatted_address"])

    # init
    s = requests.session()
    headers = {}
    curr_time = datetime.datetime.now()

    # login
    login_data = {
        "username": username,
        "password": password,
    }
    r = s.post(
        "https://cas.bjut.edu.cn/login",
        data=login_data,
        headers=headers,
    )
    tmp = "【登录】" + r.json()["m"]
    print(tmp)
    if not "成功" in r.text:
        time.sleep(3)
        exit()

    # report
    _data = {
        code: 20000,
        data: [
            {"question_id": 48, "answer": {"id": 112, "text": null}},
            {"question_id": 49, "answer": {"id": 113, "text": "空位置异常"}},
            {"question_id": 50, "answer": {"id": 114, "text": null}},
            {"question_id": 51, "answer": {"id": 118, "text": null}},
            {"question_id": 52, "answer": {"id": 121, "text": null}},
            {"question_id": 54, "answer": {"id": 126, "text": null}},
            {"question_id": 56, "answer": {"id": 130, "text": null}},
            {"question_id": 58, "answer": {"id": 134, "text": null}},
            {"question_id": 64, "answer": {"id": 145, "text": null}},
            {"question_id": 65, "answer": {"id": 149, "text": null}},
            {"question_id": 67, "answer": {"id": 152, "text": null}},
            {"question_id": 93, "answer": {"id": 240, "text": null}},
            {"question_id": 94, "answer": {"id": 244, "text": null}},
            {"question_id": 75, "answer": {"id": 183, "text": null}},
            {"question_id": 95, "answer": {"id": 252, "text": null}},
        ],
        error: "",
        message: "success",
        success: true,
    }

    r = s.post(
        "https://yqfk.bjut.edu.cn/api/home/daily_form", data=_data, headers=headers
    )

    r.raise_for_status()
    if r.status_code != 200:
        print("Err: Login failed!")
    if str(r.json()["e"]) == "0":
        notification(r.json()["m"])
