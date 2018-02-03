import unittest
from scraper import get_soup
from scraper import find
import requests
import re
from bs4 import BeautifulSoup
import urllib2

class TestUM(unittest.TestCase):


	def test_api_key(self):
		'''
		test case to check if the api key being extracted from the website is valid for further operations
		'''
		url = 'https://www.flickr.com/search?q=flickr'
		url2 = 'https://www.flickr.com/search?q=quasa'
		header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
		res = get_soup(url,header)
		api_key_regex = 'root.YUI_config.flickr.api.site_key = "(.*?)";'
		urls_api_key = re.search(api_key_regex, str(res)).group(1)
		res2 = get_soup(url2,header)
		api_key_regex2 = 'root.YUI_config.flickr.api.site_key = "(.*?)";'
		urls_api_key2 = re.search(api_key_regex, str(res2)).group(1)
		self.assertEqual(urls_api_key, urls_api_key2)

	def test_find(self):

		'''
		test case to check if find function is returing right values from json
		'''
		
		test_json = {"menu": {
		"id": "file",
		"value": "File2",
		"popup": {
		"menuitem": [
		{"value": "New", "onclick": "CreateNewDoc()"},
		{"value": "Open", "onclick": "OpenDoc()"},
		{"value": "Close", "onclick": "CloseDoc()"}]}}}

		test_check = (list(find('value', test_json)))

		self.assertEqual(test_check, ['New', 'Open', 'Close', 'File2'])




if __name__ == '__main__':

	unittest.main()
