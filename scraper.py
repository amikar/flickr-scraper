import requests
import re
from bs4 import BeautifulSoup
import urllib2
import string
import json
import time
import threading
import os
import sqlite3


'''
Get the html using beautifulsoup, not a needed wrapper since its being used only once at the moment. can be erased in the future
'''

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),"html.parser")

'''
find the particular element from requests as json
'''
def find(key, dictionary):
    for key_item, vert in dictionary.iteritems():
        if key_item == key:
            yield vert
        elif isinstance(vert, dict):
            for result in find(key, vert):
                yield result
        elif isinstance(vert, list):
            for dicto in vert:
                for result in find(key, dicto):
                    yield result

'''
save image by takings its final name, file will be saved according to its name
'''

def save_image(url, fname):
    r = requests.get(url, stream=True)
    with open(fname, 'a') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
        return True
    return False

'''
get all the images present in the particular page, takes the number of pages as argument to decide how many pages
you want to be quried and have the images extracted from
link is designed to load 500 images per page, does not go higher
'''

def get_image_list(clean_query,urls_api_key,urls_reqID,total_pages):
	original_name = clean_query.replace('%20', '-')

	if not os.path.isdir(IMG_DIR):
			os.makedirs(IMG_DIR % original_name)
	
	for i in range(1,9): #change range(1,total_pages) for all images , flickr loads only 4000 images on its server for any given search so ideal is range (1,9)
		page_number = str(i)

		#hard coding the ajax call , can be extracted from search_url

		response = requests.get('https://api.flickr.com/services/rest?sort=relevance&parse_tags=1&content_type=7&extras=can_comment%2Ccount_comments%2Ccount_faves%2Cdescription%2Cisfavorite%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cpath_alias%2Crealname%2Crotation%2Curl_c%2Curl_l%2Curl_m%2Curl_n%2Curl_q%2Curl_s%2Curl_sq%2Curl_t%2Curl_z&per_page=500&page='+page_number+'&lang=en-US&text='+clean_query+'&viewerNSID=&method=flickr.photos.search&csrf=&api_key='+urls_api_key+'&format=json&hermes=1&hermesClient=1&reqId='+urls_reqID+'&nojsoncallback=1').json()
		
		#photos_data = (response['photos']['photo'][0]['url_sq'])
		
		 #important piece of code to make the directories for image (remember to add rewriting images)
		photos_data = (list(find('url_l', response))) #replace url_sq with url_l for high def images
		
		for img_file in photos_data:

			'''
			take image link to extract the name 
			for flickr images https:\/\/farm8.staticflickr.com\/7101\/26278960313_64709fce17_b.jpg 
			26278960313 is its photo_id
			64709fce17_b is its name _b is the quality of image (_b is high)
			_s is for small sized images 

			'''
			img_name_regex = '_(.*?)_b.jpg' #change _s to _b if using url_l in photos_data
			img_name = re.search(img_name_regex, str(img_file)).group(1)
			img_fname = IMG_FNAME % (original_name,img_name)

			photo_id_regex = '(.*?)_'
			photo_fid = re.search(photo_id_regex, str(img_file.split("/")[-1])).group(1)



			get_location_with_name(photo_fid,urls_api_key,urls_reqID)
			save_image(img_file,img_fname)
		
		'''
			#code where multithreading can be implemented to be tried with a better db than sqlite3

			p = threading.Thread(target =get_location_with_name, args=(photo_fid,urls_api_key,urls_reqID,) )
			p.start()

			s = threading.Thread(target = save_image, args = (img_file,img_fname))
			s.start()
		'''

'''
#if one wants to search a term through console
#str(raw_input('Enter a search term: ')).replace(' ', '_')
'''

'''
the url to find the location of items, not every image would have this particular data. 
can be automated to extract data or use geocoder to find using latitude and longitude
loc_response['photo']['location']['latitude']
loc_response['photo']['location']['longitude'] 
-(makes things slower upon test)
Thread deadlock can occur, better implementation needed 
check_same_thread=False temperory implementation 
'''

def get_location_with_name(photo_id,urls_api_key,urls_reqID):
		img_title = ''
		region = ''

		#hard coding the ajax call , can be extracted from response in get_image_list

		loc_response = requests.get('https://api.flickr.com/services/rest?datecreate=1&extras=sizes%2Cicon_urls%2Cignored%2Crev_ignored%2Crev_contacts%2Cvenue%2Cdatecreate%2Ccan_addmeta%2Ccan_comment%2Ccan_download%2Ccan_share%2Ccontact%2Ccount_comments%2Ccount_faves%2Ccount_views%2Cdate_taken%2Cdate_upload%2Cdescription%2Cicon_urls_deep%2Cisfavorite%2Cispro%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cowner_datecreate%2Cpath_alias%2Crealname%2Crotation%2Csafety_level%2Csecret_k%2Csecret_h%2Curl_c%2Curl_f%2Curl_h%2Curl_k%2Curl_l%2Curl_m%2Curl_n%2Curl_o%2Curl_q%2Curl_s%2Curl_sq%2Curl_t%2Curl_z%2Cvisibility%2Cvisibility_source%2Co_dims%2Cis_marketplace_printable%2Cis_marketplace_licensable%2Cpubliceditability%2Cstatic_maps&photo_id='+photo_id+'&static_map_zoom=3%2C6%2C14&static_map_width=245&static_map_height=100&viewerNSID=&method=flickr.photos.getInfo&csrf=&api_key='+urls_api_key+'&format=json&hermes=1&hermesClient=1&reqId='+urls_reqID+'&nojsoncallback=1').json()
		if 'photo' in loc_response:
			img_title = loc_response['photo']['title']['_content']
			if 'location' in loc_response['photo']:
				region = loc_response['photo']['location']['region']['_content']
				db = sqlite3.connect('./my.db', check_same_thread=False)
				cursor2 = db.cursor()
				cursor2.execute('''INSERT INTO users(Title,Region) VALUES(?,?)''',(img_title,region))
				db.commit()

			else:
				print 'No Image information'
			

		else:
			print 'No data available'
		

# key and reqid, key expries so better to take key from page everytime
#print urls_api_key
#print urls_reqID




#get_image_list(search_term,urls_api_key,urls_reqID,total_pages)

'''
root.YUI_config.flickr.api.site_key = stores the api key to be used (usually expires after a mentioned time)
root.reqId = also important to get from site
total_pages can be really high but flickr loads only 4000 images per item and starts repeating images once we have
got 4000
tried with advanced search and got the same result
keep total_pages in code to scale further if possible
'''


def get_page_info(keywords):

	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

	clean_query = keywords.replace(' ', '%20')

	search_url = 'https://www.flickr.com/search?q='+clean_query

	soup = get_soup(search_url,header)

	total_imgs_unclean = soup.find(class_='view-more-link').text
	
	api_key_regex = 'root.YUI_config.flickr.api.site_key = "(.*?)";'
	urls_api_key = re.search(api_key_regex, str(soup)).group(1)

	api_reqID_regex = 'root.reqId = "(.*?)";'
	urls_reqID = re.search(api_reqID_regex, str(soup)).group(1)
	total_imgs =  int(string.split(total_imgs_unclean," ")[-1].replace(",", ""))

	total_pages = total_imgs/500
	
	get_image_list(clean_query,urls_api_key,urls_reqID,total_pages)


'''
take each term from keyword.txt and initiate a thread of each term
'''

def keywords_search(keywords):
	for i,search_term in enumerate(keywords):
		t = threading.Thread(target=get_page_info, args=(search_term,))
		t.start()

'''
keeps adding data to the same table if table exists, might not be a good thing based on needs
console -
-> sqlite3 my.db
-> .tables
-> select * from users
'''

if __name__ == '__main__':
	photos_data = []
	IMG_FNAME = './images/%s/%s.jpg'
	IMG_DIR = './images/%s'
	keywords = []
	db = sqlite3.connect('./my.db')
	cursor = db.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, Title TEXT,Region TEXT)''')
	db.commit()
	cursor.close()
	db.close()
	with open('keywords.txt') as f:
		keywords = [e.strip() for e in f.readlines()]
	keywords_search(keywords)


