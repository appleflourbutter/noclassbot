import urllib2
from bs4 import BeautifulSoup

html = urllib2.urlopen("https://campus.icu.ac.jp/public/ehandbook/DisplayNoClass.aspx")

soup = BeautifulSoup(html, "html5lib")
print html

td_list = soup.find_all("span", id="ctl00_ContentPlaceHolder1_grv_no_class_ctl02_lb_Date")
print td_list
