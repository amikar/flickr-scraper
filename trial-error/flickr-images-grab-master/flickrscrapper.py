import requests
import re

# Asks for a search term
search_term = str(raw_input('Enter a search term: ')).replace(' ', '_')
# Appends search term to url
search_url = 'https://www.flickr.com/search?q=paris:100000'

#'http://www.flickr.com/search/?text={}'.format(search_term)+'&view_all=1000'

r = requests.get(search_url)
html = r.content.replace('\n','').replace('\t','')

# using re to grab pic urls from html - had to look through the html
imgs = 'background-image: url\(//(.+?)\)"'
pattern = re.compile(imgs)
img_urls = re.findall(pattern, html)

print len(img_urls)


# save top 10 results to file
#for i in img_urls[:500]:
#    r = requests.get('http://'+i)
#    with open(i.replace('/','_'), 'wb') as f:
#        f.write(r.content)