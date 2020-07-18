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
    username = "********"
    password = "********"

    # init
    s = requests.session()
    headers = {}
    curr_time = datetime.datetime.now()

    # login
    data = {"username": username, "password": password}
    r = s.post(
        "https://itsapp.bjut.edu.cn/uc/wap/login/check", data=data, headers=headers
    )
    tmp = "【登录】" + r.json()["m"]

    # report
    data = {"tw": "1"}

    go_on = True

    if go_on:
        r = s.post(
            "https://itsapp.bjut.edu.cn/xisuncov/wap/open-report/save",
            data=data,
            headers=headers,
        )
        tmp = "【上报】" + json.loads(r.text)["m"]
        print(tmp)
        r.raise_for_status()
        if r.status_code != 200:
            err = "Err: Login failed!"
            print(err)
            notification(err)

        if str(r.json()["e"]) == "0":
            notification(r.json()["m"])
