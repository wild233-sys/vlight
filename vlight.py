# -*- coding:utf-8 -*-
#import datetime
import ntplib
import time
def config(v1,v2,v3,v4):
    global time_sn_interval,time_ew_interval,position,yellow_light_time
    time_sn_interval=int(v1)#南北方向绿灯时长
    time_ew_interval=int(v2)#东西方向绿灯时长
    position=v3#所处道路朝向（sn南北，ew东西）
    yellow_light_time=int(v4)#黄灯时长
def ntp_check():#检测ntp服务器有效性
    global response,available,last_check
    client = ntplib.NTPClient()
    for i in range (1,8):
        try:
            response = client.request('time'+str(i)+'.aliyun.com')
            last_check=0
            available=('time'+str(i)+'.aliyun.com')
            break
        except:
            response = client.request("cn.ntp.org.cn")
            last_check=0
            available=("cn.ntp.org.cn")
            continue
def network():#检测网络有效性
    global available
    try:
        print("已选择授时服务器："+available)
        time.sleep(1)
    except:
        while True:
            key=str(input('''
时间获取失败，可能是网络原因导致，现在要:
[1]重试
[2]使用电子设备系统时间
'''))
            if "1"==key:
                ntp_check()
                network()
                break
            elif "2"==key:
                break
            else:
                print("输入错误")
                continue
def time_get():#获取时间
    global response,precise_time
    try:
        precise_time=round(int(response.tx_time))
    except:
        precise_time=time.time()
    finally:
        precise_time=int(precise_time)
def light_status():#判断路灯状态
    global precise_time,time_sn_interval,time_ew_interval,position,yellow_light_time
    time_range=precise_time%(time_sn_interval+time_ew_interval+yellow_light_time)
    if position=="sn" and 0<=time_range<time_sn_interval:
        return "g"
    elif  position=="ew" and (time_sn_interval+yellow_light_time)<=time_range<(time_sn_interval+time_ew_interval+yellow_light_time):
        return "g"
    elif position=="sn" and (time_sn_interval+yellow_light_time)<=time_range<(time_sn_interval+time_ew_interval+yellow_light_time):
        return "r"
    elif position=="ew" and 0<=time_range<time_sn_interval:
        return "r"
    else:
        return "y"

 
def time_left():
    global precise_time,time_sn_interval,time_ew_interval,position,yellow_light_time
    l_light_status=light_status()
    time_range=precise_time%(time_sn_interval+time_ew_interval+yellow_light_time)
    if position=="sn" and l_light_status=="r":
        return time_sn_interval+yellow_light_time+time_ew_interval-time_range+yellow_light_time
    if position=="ew" and l_light_status=="g":
        return time_sn_interval+yellow_light_time+time_ew_interval-time_range
    if position=="sn" and l_light_status=="g":
        return time_sn_interval-time_range
    if position=="ew" and l_light_status=="r":
        return time_sn_interval-time_range+yellow_light_time
    if l_light_status=="y":
        L1=time_sn_interval+yellow_light_time-time_range
        return L1
def status():
    global ls,tl
    l_light_status=light_status()
    l_time_left=time_left()
    ls=l_light_status
    tl=l_time_left
    if l_light_status=="r":
        return "现在是【红】灯，还剩下【"+str(l_time_left)+"】秒"
    elif l_light_status=="g":
        return "现在是【绿】灯，还剩下【"+str(l_time_left)+"】秒"
    elif l_light_status=="y":
        return "现在是【黄】灯，还剩下【"+str(l_time_left)+"】秒"
def container():
    global ls,tl,position,time_sn_interval,time_ew_interval
    tl=int(tl)-1
    if tl<=0:
        if ls=="r":
            ls="g"
        elif ls=="g":
            ls="y"
            tl=5
        elif ls=="y":
            ls="r"
        if position=="sn" and ls=="r":
                tl=time_ew_interval+yellow_light_time
        if position=="ew" and ls=="g":
                tl=time_ew_interval
        if position=="sn" and ls=="g":
                tl=time_sn_interval
        if  position=="ew" and ls=="r":
                tl=time_sn_interval+yellow_light_time
    if ls=="r":
        return "现在是【红】灯，还剩下【"+str(tl)+"】秒"
    elif ls=="g":
        return "现在是【绿】灯，还剩下【"+str(tl)+"】秒"
    elif ls=="y":  
        return "现在是【黄】灯，还剩下【"+str(tl)+"】秒"
def main():
    global last_check
    #config(60,40,"sn",5)
    config(input("东西方向绿灯时间"),input("南北方向绿灯时间"),input("道路方向（sn南北，ew东西）"),input("黄灯时间"))
    ntp_check()
    network()
    time_get()
    print(status())
    time.sleep(1)
    last_check=last_check+1
    while True:
        print(container())
        last_check=last_check+1
        time.sleep(1)
        if last_check>180:
            print("连续三分钟闲置，重新校准时间")
            ntp_check()
            network()
            time_get()
            print(status())
            time.sleep(1)
            last_check=last_check+1
if __name__ == '__main__':
    main()
        
    
