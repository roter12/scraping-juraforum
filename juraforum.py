import os
import sys
import time
import json
import argparse
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


# Save as a file
def save_file(text, filename = 'test.tmp'):
	if type(text) != 'str':
		text = str(text)
	file = open(filename, "w", encoding="utf-8")
	file.write(text)
	file.close()

# Read file
def read_file(filename = 'test.tmp'):
    file = open(filename, "r", encoding="utf-8")
    text = file.read()
    file.close()
    return text

# Save as json
def save_json_file(json_value, file_path):
    with open(file_path, "a") as file:
        # Write the JSON data to the file
        json.dump(json_value, file)


# Get html content
driver = webdriver.Chrome()
def get_html_with_request(url):
	global driver
	time.sleep(3)
	driver.get(url)
	return driver.page_source

# Parsing page links
def parse_page_links(html):
    links = []
    soup = BeautifulSoup(html, "html.parser")
    for f in soup.findAll('div', attrs={'class':'structItem'}):
        el = f.find('a')
        if el != None:
            links.append(el["href"])
            print("Article link: ", el["href"])
    return links

# Parsing one page
def parse_one_page(html):
    ret = {"title":"", "answers":[]}
    soup = BeautifulSoup(html, "html.parser")
    
    el = soup.find('h1', attrs={'class':'p-title-value'})
    ret["title"] = el.string if el != None else ""
    print(ret["title"])

    for div in soup.findAll('div', attrs={'class':'bbWrapper'}):
        article = div.get_text()
        if "question" in ret:
            ret["answers"].append(article)
        else:
            ret["question"] = article
    
    return ret


# Get first page
origin_url = "https://www.juraforum.de"
base_url = "https://www.juraforum.de/forum/f/arbeitsrecht/"
html = get_html_with_request(base_url)
#save_file(get_html_with_request(base_url))
#html = read_file()
soup = BeautifulSoup(html, "html.parser")

# Get page count
maxe = soup.find('input', attrs={'class':'input input--number js-numberBoxTextInput input input--numberNarrow js-pageJumpPage'})
if maxe == None:
    print("Failed to get page count!")
    exit(1)
end_page = int(maxe["max"])

# Parse argument
argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--start_page", help="Start page number")
argParser.add_argument("-e", "--end_page", help="End page number")
args = argParser.parse_args()
start_page = int(args.start_page) if args.start_page else 1

if args.end_page and int(args.end_page) < end_page:
    end_page = int(args.end_page)
print(f"Page range: {start_page} ~ {end_page}")

# Extract href
results = []
for i in range(start_page, end_page+1):
    print(f"Scraping links from {i} page...")
    links = []
    if i > 1:
        url = base_url + str(i+1)
        print(f"url: {url}")
        html = get_html_with_request(url)
    links.extend(parse_page_links(html))
    
    for link in links:
        url = origin_url + link
        print(f"Scraping article page: {url}")
        html = get_html_with_request(url)
        #save_file(html, "page.tmp")
        #html = read_file("page.tmp")
        results.append(parse_one_page(html))

        save_json_file(results, "result.json")

        file = open('link.log', 'a')
        file.write(f"{link}\n")
        file.close()

print("\nSaved to result.json")