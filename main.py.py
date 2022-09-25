import requests
import re
import os

import argparse
from bs4 import BeautifulSoup


try:
    os.remove("Emails.txt")
except:
    pass

parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", dest="url", help="URL you would like to analyze", required=True)
params = parser.parse_args()

print("Searching...")
print("This may take a few seconds")

reqs = requests.get(params.url)
soup = BeautifulSoup(reqs.text, 'html.parser')

urls = []
for link in soup.find_all('a'):
    urls.append(link.get('href'))

new_urls = []
for new_url in urls:
    new_url = str(new_url)
    match = re.findall(r"http[s]?", new_url, re.I)
    if match:
        new_urls.append(new_url)
    else:
        new_link = "https://www.fcfm.uanl.mx" + new_url
        new_urls.append(new_link)


new_urls = list(set(new_urls))

final_list = []
for URL_look in new_urls:
    try:
        response = requests.get(URL_look)
        if response.status_code != 200:
            exit()

        regExMail = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
        new_emails = re.findall(regExMail, response.text, re.I)
        final_list = final_list+new_emails

    except:
        pass

final_list = list(set(final_list))
with open("Emails.txt", "a") as file:
    for email in final_list:
        file.write(email+"\n")


print("\nSearch successful")

