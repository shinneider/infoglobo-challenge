import feedparser
from bs4 import BeautifulSoup
from app.shared.logger import Logger


def parse_summary_json(raw):
    """
        Parse HTML summary para json format 
        formatter specs: (map html tags in a json)
            tag p -> dict with `type` = `text` and `content` = "tag content"
            tag div//img -> dict with `type` = `image` and `content` = "img src"
            tag div//ul -> dict with `type` = `links` and `content` = /
                                                    ["all href's links in list"]
    """
    Logger.info('started summary parse')
    content = []

    soup = BeautifulSoup(raw, "html.parser")
    for element in soup.find_all(['div', 'p']):
        if element.text.strip() == '': continue

        if element.name == 'p':
            content.append({
                'type': 'text',
                'content': element.text.strip()
            })

        elif element.name == 'div' and element.find('img'):
            content.append({
                'type': 'image',
                'content': element.img.get('src')
            })

        elif element.name == 'div' and element.find('ul'):
            links = element.find_all('a')
            content.append({
                'type': 'links',
                'content': [link.get('href') for link in links]
            })

        else:
            Logger.warning(
                f'Unexpected element: {element.name}, text: {element.text.strip()}'
            )

    Logger.info('Finish summary parse')
    return content

def parse_feed_json(raw):
    """
        Parse feed to json format
        formatter specs: (map each entry to json)
            title -> feed entry title
            link -> feed entry link
    """
    Logger.info(f'Started parse data')

    entries = feedparser.parse(raw).get('entries', None)
    if not entries or not isinstance(entries, list):
        Logger.error('Root of data is invalid')
        return False, []


    status, items = True, []
    entry_keys = ['title', 'link', 'summary']
    for entry in entries:
        if not all(key in entry for key in entry_keys):
            Logger.error('Entry is invalid')
            status = False
            break

        items.append({
            'title': entry['title'],
            'link': entry['link'],
            'content': parse_summary_json(entry['summary'])
        })


    Logger.info(f'Finish parse data')
    return status, items