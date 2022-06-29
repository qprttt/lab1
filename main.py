import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote


links_visited = set()


def parse_url(url_in, url_find, session, depth=0):
    if url_in == url_find:
        print(unquote(url_in))
        return url_in
    links_visited.add(url_in)
    
    if depth == 5:
        return

    WIKI_URL = url_in.split('/wiki/')[0]
    response = session.get(url_in)
    content = BeautifulSoup(response.text, 'html.parser').find(id="mw-content-text")

    navigation = content.find_all(attrs={'role': 'navigation'})
    for block in navigation:
        block.decompose()
    a_tags = content.find_all('a', attrs={'href': re.compile("^/wiki/")})

    links = (link['href'] for link in a_tags if link.has_attr('href'))
    wiki_links = (WIKI_URL + link for link in links if link.startswith("/wiki/"))
    links_filtered = (link for link in wiki_links if link not in links_visited)

    for link in links_filtered:
        found = parse_url(link, url_find, session, depth=depth+1)
        if found:
            print(unquote(url_in))
            return url_in
    return


def main(url_in, url_find):
    
    session = requests.session()
    
    response = session.get(url_in)
    url_in = str(response.url)

    response = session.get(url_find)

    url_find = str(response.url)
    answer = parse_url(url_in, url_find, session)

    if not answer:
        print('Путь не найден')


if __name__ == '__main__':
    url_start = "https://en.wikipedia.org/wiki/Six_degrees_of_separation"
    url_end = "https://en.wikipedia.org/wiki/American_Broadcasting_Company"
    main(url_start, url_end)
