#!/usr/bin/env python

import sys
import requests
import re
from bs4 import BeautifulSoup

BASE_URL = 'https://www.destroyallsoftware.com'

def download_file(url, episode_num, total_episodes, title):
    local_filename = re.match(r'^.*\.com/(.*)\?.*$', url).group(1)
    with open(local_filename, 'wb') as f:
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')
        if total_length is None:
                f.write(r.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in r.iter_content(chunk_size=4096):
                if data:
                    dl += len(data)
                    f.write(data)
                    done = float(dl)/float(total_length)
                    sys.stdout.write("(%d%%) Downloading episode [%d/%d] %s...                       \r" % (
                        int(done*100), 
                        episode_num, 
                        total_episodes, 
                        title))
                    sys.stdout.flush()
        return local_filename

def main():
    r = requests.get('https://www.destroyallsoftware.com/screencasts/catalog/')
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')

    episodes = soup.find_all('div', {'class':'episode'})
    for i, e in enumerate(episodes):
        r = requests.get(BASE_URL + e.a['href'])
        html = r.content
        e_soup = BeautifulSoup(html, 'html.parser')
        title = e_soup.find('h2', {'class': 'title'}).text
        match = re.search(r'source.src = "(.*1080p\.mp4.*)"', html)
        if not match:
            match = re.search(r'source.src = "(.*)"', html)
        saved_file = download_file(match.group(1), i+1, len(episodes), title)

        
if __name__ == '__main__':
    main()
