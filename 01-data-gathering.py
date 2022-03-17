"""
Using Beautiful Soup I will grab and store the data for each episode in Campaign 3 in a cvs
"""

# Imports 
import requests
from bs4 import BeautifulSoup
import re

URL = "https://kryogenix.org/crsearch/html/index.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


# Grab the links for all campaign 3 episodes and store them into a list
results= soup.find_all('a',{'href':re.compile(r'^cr3')})

links=[link['href'] for link in results]

# Check we got them 
#print(links)

scripts=[]

for link in links:
    URL="https://kryogenix.org/crsearch/html/"+link
    page=requests.get(URL)
    soup=BeautifulSoup(page.content,"html.parser")

    # Grab all the lines spoken
    results= soup.findAll('div',id="lines")[0].text.strip()
    # Returned is a giant string... Now I want to split the string by who is talking
    lines=[]
    for line in results.split('#'):
        line = line.replace("→\n", " ")
        date_regex = r"\d+/\d+/\d+" # remove dates in the format 00/00/0000
        punct_regex = r"[^0-9a-zA-Z\s]" # any non-alphanumeric chars
        special_chars_regex = r"[\$\%\&\@\n+]" # any speical chars
        numerical_regex = r"\d+" # any remianing digits 
        multiple_whitespace = " {2,}" # any 2 or more consecutive white spaces (don't strip single white spaces!)

        line = re.sub(date_regex, " ", line)
        line = re.sub(punct_regex, " ", line)
        line = re.sub(special_chars_regex, " ", line)
        line = re.sub(numerical_regex, " ", line)
        line = re.sub(multiple_whitespace, " ", line)

        if line=='':
            pass
        elif line[0] ==' ':
            line = line[1:]
            if line[-1] ==' ':
                line=line[:-2]
            lines.append(line.lower())
    scripts.append(lines)

#print(scripts[0][:6])

