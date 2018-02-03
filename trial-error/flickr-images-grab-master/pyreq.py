from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),"html.parser")



query = raw_input("")# you can change the query for the image  here
image_type="Country"
query= query.split()
query='+'.join(query)
url="https://www.flickr.com/search/?text=paris" #+query
print url
#add the directory for your image here
DIR="/data'"+(query.split('+'))[0]+"\\"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url,header)


ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("a",{"class":"overlay"}):
    link , Type =json.loads(a.text)["href"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print  ActualImages#"there are total" , len(ActualImages),"images"


###print images
for i , (img , Type) in enumerate( ActualImages):
    try:
        req = urllib2.Request(img, headers={'User-Agent' : header})
        raw_img = urllib2.urlopen(req).read()
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print cntr
        if len(Type)==0:
            f = open(DIR + image_type + "_"+ str(cntr)+".jpg", 'wb')
        else :
            f = open(DIR + image_type + "_"+ str(cntr)+"."+Type, 'wb')


        f.write(raw_img)
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e