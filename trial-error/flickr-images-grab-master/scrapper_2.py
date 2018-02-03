import requests
from requests import Session
import re
from bs4 import BeautifulSoup
import urllib2
import string
import json


header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),"html.parser")

def unjsonpify(jsonp):
    return jsonp[14:-1]

# Asks for a search term
search_term = 'paris' #str(raw_input('Enter a search term: ')).replace(' ', '_')
# Appends search term to url

search_url = 'https://www.flickr.com/search?q='+search_term

soup = get_soup(search_url,header)
total_imgs_unclean = soup.find(class_='view-more-link').text

api_key_regex = 'root.YUI_config.flickr.api.site_key = "(.*?)";'
urls_api_key = re.search(api_key_regex, str(soup)).group(1)

api_reqID_regex = 'root.reqId = "(.*?)";'
urls_reqID = re.search(api_reqID_regex, str(soup)).group(1)

#print urls_api_key
#print urls_reqID


total_imgs =  int(string.split(total_imgs_unclean," ")[-1].replace(",", ""))

x = total_imgs/500
photos_data = []
photo_title = []

def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

def get_image_list(search_term,urls_api_key,urls_reqID,x):
	for i in range(1):
		page_number = str(i)
		response = requests.get('https://api.flickr.com/services/rest?sort=relevance&parse_tags=1&content_type=7&extras=can_comment%2Ccount_comments%2Ccount_faves%2Cdescription%2Cisfavorite%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cpath_alias%2Crealname%2Crotation%2Curl_c%2Curl_l%2Curl_m%2Curl_n%2Curl_q%2Curl_s%2Curl_sq%2Curl_t%2Curl_z&per_page=500&page='+page_number+'&lang=en-US&text='+search_term+'&viewerNSID=&method=flickr.photos.search&csrf=&api_key='+urls_api_key+'&format=json&hermes=1&hermesClient=1&reqId='+urls_reqID+'&nojsoncallback=1').json()
		
		photo_title.append(list(find('title', response)))

		#photos_data = (response['photos']['photo'][0]['url_sq'])


		photos_data.append(list(find('url_sq', response)))

		print photos_data
		"""
		f = open('images.txt','w')
		f.write(str(photo_title))

		f.seek(0)

		f.close()
		"""

get_image_list(search_term,urls_api_key,urls_reqID,x)
