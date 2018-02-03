# flickr-scraper
A scraper for flickr where we use only beautiful soup and requests to handle scraping images. We do not use the flickr api or browser tools like selenium. 

run python Scraper.py in console. it should give you the first 4000 images the 4001 image would be the same as the 1st image. 

It handles lazy load by using the javascript instantiated when we scroll down the page. 

Add to "keywords.txt" to change or increase the things you wants to scrape for.

Delete the folders of pre stored images for the particular title if you want to download them again.
uses multithreading to create a thread for each instance of keywords and scrapes them individually. 


-----------------------------------------------------------------------------------------------------------------
Copyright (c) <2018> <Amikar Divij>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
