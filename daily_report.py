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
    username = "*******"
    password = "*******"

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
    data = {"username": username, "password": password}
    r = s.post(
        "https://itsapp.bjut.edu.cn/uc/wap/login/check", data=data, headers=headers
    )
    tmp = "【登录】" + r.json()["m"]
    print(tmp)
    if not "成功" in r.text:
        time.sleep(3)
        exit()

    # report
    data = {
        "ismoved": "0",
        "dqjzzt": "0",  # 当前居住状态，0在校、1在京不在校
        "jhfjrq": "",  # 计划返京日期
        "jhfjjtgj": "",  # 计划返京交通工具
        "jhfjhbcc": "",  # 计划返京航班车次
        "tw": 1,  # 体温范围所对应的页面上的序号（下标从 1 开始）
        "sfcxtz": "0",  # 今日是否出现发热、乏力、干咳、呼吸困难等症状？
        "sfjcbh": "0",  # 今日是否接触疑似/确诊人群？
        "sfcxzysx": "0",  # 是否有任何与疫情相关的注意事项？
        "qksm": "",  # 情况说明
        "sfyyjc": "0",  # 是否医院检查
        "jcjgqr": "0",  # 检查结果确认
        "remark": "",
        "address": location["regeocode"]["formatted_address"],
        "geo_api_info": json.dumps(
            {
                "type": "complete",
                "info": "SUCCESS",
                "status": 1,
                "position": {"O": lng, "P": lat, "lng": lng, "lat": lat},
                "message": "Get geolocation success.Convert Success.Get address success.",
                "location_type": "html5",
                "accuracy": random.randint(10, 100),
                "isConverted": True,
                "addressComponent": location["regeocode"]["addressComponent"],
                "formatted_address": location["regeocode"]["formatted_address"],
                "roads": [],
                "crosses": [],
                "pois": [],
            },
            ensure_ascii=False,
        ),
        "area": "北京市  " + location["regeocode"]["addressComponent"]["district"],
        "province": "北京市",
        "city": "北京市",
        "sfzx": "0",  # 是否已经返校
        "sfjcwhry": "0",  # 是否接触武汉人员
        "sfjchbry": "0",  # 是否接触湖北人员
        "sfcyglq": "0",  # 是否处于隔离期
        "gllx": "",  # 隔离类型
        "glksrq": "",  # 隔离开始日期
        "jcbhlx": "",  # 接触病患类型
        "jcbhrq": "",  # 接触病患日期
        "bztcyy": "",  # 当前地点与上次不在同一城市，原因如下：2 探亲, 3 旅游, 4 回家, 1 其他
        "sftjhb": "0",  # 是否停经湖北
        "sftjwh": "0",  # 是否停经武汉
        "sfsfbh": "0",  # 是否所在省份变化
        "xjzd": "",  # 现居住地
        "jcwhryfs": "",  # 接触武汉人员方式
        "jchbryfs": "",  # 接触湖北人员方式
        "szgj": "",  # 所在国家
        "jcjg": "",  # 检查结果
        # --- The following are uncommented field --- #
        "date": datetime.datetime.now().strftime("%Y%m%d"),
        # 'uid': '0',
        "created": int(time.time()),
        "jcqzrq": "",
        "sfjcqz": "",
        "szsqsfybl": 0,
        "sfsqhzjkk": 0,
        "sqhzjkkys": "",
        "sfygtjzzfj": 0,
        "gtjzzfjsj": "",
        "ljrq": "",
        "ljjtgj": "",
        "ljhbcc": "",
        "fjrq": "",
        "fjjtgj": "",
        "fjhbcc": "",
        "fjqszgj": "",
        "fjq_province": "",
        "fjq_city": "",
        "fjq_szdz": "",
        "jrfjjtgj": "",
        "jrfjhbcc": "",
        "fjyy": "",
        "szsqsfty": "",
        "sfxxxbb": "",
        "created_uid": 0,
        # 'id': 0,
        "gwszdd": "",
        "sfyqjzgc": "",
        "jrsfqzys": "",
        "jrsfqzfy": "",
    }

    r = s.post(
        "https://itsapp.bjut.edu.cn/ncov/wap/default/save", data=data, headers=headers
    )

    r.raise_for_status()
    if r.status_code != 200:
        print("Err: Login failed!")
    if str(r.json()["e"]) == "0":
        notification(r.json()["m"])
