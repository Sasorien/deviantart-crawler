###############################################
# Usage: Crawler for deviantart user gallery and download "Full View" version
# Developer: Mohammed AlYousef (blux1987@gmail.com)
###############################################

from bs4 import BeautifulSoup
import urllib2
import os
import sys


def html_from_URL(site_url):
	usock = urllib2.urlopen(site_url)
	html = usock.read()
	usock.close()
	
	return html

def get_all_links(source):
	soup = BeautifulSoup(source)
	links = []
	for link in soup.find_all("a", class_="t"):
		links.append(link.get("href"))
	return links

def get_image(source):
	soup = BeautifulSoup(source)
	links = []
	for link in soup.find_all("img", class_="fullview"):
			links.append(link.get("src"))
	return links

def get_pages_count(source):
	soup = BeautifulSoup(source)
	# last_page_link = ""
	max = 0
	for link in soup.find_all("a", attrs={"name":"gmi-GPageButton", "class":"away"}, limit=3):
		offset = int(link.get("data-offset"))
		if offset > max :
			max = offset
	return max/24

def get_file_name(url):
	index = url.rfind("/")
	return url[index+1:100]

def download_file(url, name):
	try:
		file = urllib2.urlopen(url)
		output = open(name,"wb")
		output.write(file.read())
		output.close()
	except urllib2.HTTPError as e:
		print(f"<<<<<<<<<<<<<<<<<<- Error Downloading!!! ->>>>>>>>>>>>>>>>>>>>>\n{e}")

# def username(url):
# 	http = url.find("//")
# 	dot = url.find(".")
#         return url[http+2:dot]

def main(self):
	try:
		username = sys.argv[1]
	except:
		print(f"\nUsage: python {sys.argv[0]} username\n")
		exit()
		
	url = f"http://{username}.deviantart.com/gallery/""
	
	# Create dir for user
	dirname = username
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	
	page_count = get_pages_count(html_from_URL(url))
	i = 0
	print(f"page count = {str(page_count+1)}")
	
	while i <= page_count:
		offset = i*24
		myurl = f"{url}?offset={str(offset)}"
		
		myhtml = html_from_URL(myurl)
		mylinks = get_all_links(myhtml)
	
		print(f"=============== Getting Page {str(i+1)} ===============")
	
		for link in mylinks:
			myimage_page = html_from_URL(link)
			myimage = get_image(myimage_page)
		
			for image in myimage:
				filename = get_file_name(image)
				print(f"Getting {filename}")
				download_file(image, dirname+"/"+filename)
				
		print(f"Done with page {str(i+1)}\n")
		i += 1
		
	print(f"done with all pages, enjoy!")

main()