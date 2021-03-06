# coding: utf-8
import urllib
from bs4 import BeautifulSoup
import datetime
import tweepy
import sys
import json
import os

#Twitterの認証
f = open(os.path.dirname(__file__) + '/api.txt')
api = f.readlines()
f.close()
consumer_key = api[0][:-1]
consumer_secret = api[1][:-1]
access_token = api[2][:-1]
access_secret = api[3][:-1]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#
html = urllib.request.urlopen("https://campus.icu.ac.jp/public/ehandbook/DisplayNoClass.aspx")
soup = BeautifulSoup(html, "html.parser")

#日時を取得
def get_date(gap):
    date = datetime.date.today() + datetime.timedelta(days=gap)
    year = str(date.year)
    month = date.month
    day = date.day
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)

    today = year + "." + month + "." + day
    return today

table = []
num = 1
exist = 1

#とりまリストをつくる
print("making list")
while exist != None:
    num += 1
    if num < 10:
        str_num = "0" + str(num)
    else:
        str_num = str(num)
    exist = soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_lb_Date")
    if exist == None:
        break
    table.append([])
    table[num-2].append(soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_lb_Date").string)
    table[num-2].append(soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_lb_Period").string)
    table[num-2].append(soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_lb_CourseNo").string)
    table[num-2].append(soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_lb_Title").string)
    table[num-2].append(soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_Label1").string)
    table[num-2].append(soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_lb_Instructor").string)
    table[num-2].append(soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_lb_MakeUp").string)
    table[num-2].append(soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_lb_AsOf").string)
    table[num-2].append(soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_Label3").string)
    #日、時限、CourseNo、授業名英語、授業名日本語、教員、メイクアップ、？、何日付け

#print(table)

#今日の休講情報
if sys.argv[1] == "today":
    print(u"今日の休講情報をつぶやきます")
    today = get_date(0)
    #today = "2016.02.16"
    today_list = []
    #today = "2016.02.08"

    #今日の情報だけ抽出
    for one in table:
        if one[0] == today:
            today_list.append(one)

    #つぶやく
    for one in today_list:
        text2tweet =u"今日の休講情報\n" + one[2] + u" " + one[4] + u" " + one[5] + u"先生 " + one[1] + u"\n詳しくはこちらhttps://campus.icu.ac.jp/public/ehandbook/DisplayNoClass.aspx"
        print(text2tweet)
        api.update_status(text2tweet)

#明日の休講情報
elif sys.argv[1] == "tomorrow":
    print(u"明日の休講情報をつぶやきます")
    tomorrow = get_date(1)#明日の日時を取得
    tomorrow_list = []

    for one in table:
        if one[0] == tomorrow:
            tomorrow_list.append(one)

    for one in tomorrow_list:
        text2tweet =u"明日の休講情報\n" + one[2] + u" " + one[4] + u" " + one[5] + u"先生 " + one[1] + u"\n詳しくはこちらhttps://campus.icu.ac.jp/public/ehandbook/DisplayNoClass.aspx"
        print(text2tweet)
        api.update_status(text2tweet)

#新着の休講情報
elif sys.argv[1] == "new":
    print("新着の休講情報をつぶやきます")
    prev_list = []
    new_list = []

    #前回取得した情報を読み込み
    with open(os.path.dirname(__file__) + "/data.json", 'r') as f:
        prev_list = json.load(f)

    #print(prev_list)
    #print(table)

    #これなんだっけ…？なにしてるのかよくわかんない。
    if table != prev_list:
        print(1)
    else:
        print(2)

    #新旧を比較
    for one in table:
        #prev = [x for x in prev_list if x == one]
        for prev in prev_list:
            if prev == one:
                break
        else:
            new_list.append(one)
    print(new_list)

    for one in new_list:
        text2tweet =u"新着の休講情報\n" + one[2] + u" " + one[4] + u" " + one[5] + u"先生 \n" + one[0] + u" " + one[1] + u"\n詳しくはこちらhttps://campus.icu.ac.jp/public/ehandbook/DisplayNoClass.aspx"
        print(text2tweet)
        api.update_status(text2tweet)

#テスト用。特定の日時の休講情報をつぶやく
if sys.argv[1] == "day":
    set_month = sys.argv[2]
    set_day = sys.argv[3]
    print(str(set_month) + u"月" + str(set_day) + u"日の休講情報をつぶやきます")
    set_month = str(set_month)
    set_day = str(set_day)
    if len(set_month) == 1:
        set_month = "0" + set_month
    if len(set_day) == 1:
        set_month = "0" + set_day
    today = "2016." + set_month + "." + set_day
    today_list = []
    #today = "2016.02.08"

    for one in table:
        if one[0] == today:
            today_list.append(one)

    for one in today_list:
        text2tweet = str(set_month) + u"月" + str(set_day) + u"日" + u"の休講情報\n" + one[2] + u" " + one[4] + u" " + one[5] + u"先生 " + one[1] + u"\n詳しくはこちら https://campus.icu.ac.jp/public/ehandbook/DisplayNoClass.aspx"
        print(text2tweet)
        api.update_status(text2tweet)

#今回取得した情報を保存
with open(os.path.dirname(__file__) + "/data.json", 'w') as f:
    json.dump(table, f)
