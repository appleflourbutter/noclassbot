# coding: utf-8
import urllib2
from bs4 import BeautifulSoup
import datetime
import tweepy

f = open('api.txt')
api = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
f.close()
consumer_key = api[0][:-1]
print api[2][:-1]
consumer_secret = api[1][:-1]
access_token = api[2][:-1]
access_secret = api[3][:-1]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

html = urllib2.urlopen("https://campus.icu.ac.jp/public/ehandbook/DisplayNoClass.aspx")
soup = BeautifulSoup(html)

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

print "making list"
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


today = get_date(0)
today_list = []
#today = "2016.02.08"

for one in table:
    if one[0] == today:
        today_list.append(one)

print today_list

tomorrow = get_date(1)
tomorrow = "2016.02.08"
tomorrow_list = []
print tomorrow
for one in table:
    if one[0] == tomorrow:
        today_list.append(one)

print tomorrow_list

for one in tomorrow_list:
    api.update_status("明日の休講情報")

api.update_status("Twitter APIからの投稿のテストです")
