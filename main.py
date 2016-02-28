# coding: utf-8
import urllib2
from bs4 import BeautifulSoup
import datetime

html = urllib2.urlopen("https://campus.icu.ac.jp/public/ehandbook/DisplayNoClass.aspx")

soup = BeautifulSoup(html, "html5lib")
print html

table = []
num = 1

exist = 1

while exist != None:
    num += 1
    if num < 10:
        str_num = "0" + str(num)
    else:
        str_num = str(num)
    exist = soup.find("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl" + str_num + "_lb_Date")
    if exist == None:
        break
    print exist
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

date = datetime.date.today()
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
today_list = []
#today = "2016.02.08"

for one in table:
    if one[0] == today:
        today_list.append(one)

print today_list
