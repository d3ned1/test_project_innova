import json
import requests
import logging
from bs4 import BeautifulSoup
from optparse import OptionParser

FORMAT = '%(asctime)-15s %(lineno)-4d %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestParser:
    data = {
    }

    def parse(self, url):
        try:
            page_to_parse = requests.get(url)
            soup = BeautifulSoup(page_to_parse.content, 'html.parser')
        except Exception as e:
            logger.warning('Page parsing has failed with exception:')
            raise e
        try:
            self.data['charset'] = page_to_parse.encoding
        except Exception as e:
            logger.info(e)
        try:
            self.data['lang'] = soup.html['lang']
        except Exception as e:
            logger.info(e)
        if soup.title:
            self.data['title'] = soup.title.find(string=True)
        if soup.h1:
            try:
                self.data.update({'h1': {
                    'attributes': [child.attrs for child in soup.h1],
                    'image_source': soup.img['src'] if soup.img else None,
                    'overall': soup.h1.text if soup.h1 else None,
                                         }
                                  })
            except Exception as e:
                logger.info(e)
        if len(self.data) is not 0:
            json_as_result = json.dumps(self.data, indent=4, sort_keys=True, ensure_ascii=False)
            print(json_as_result)
            with open('export_file.json', 'w', encoding='utf8') as export_file:
                export_file.write(json_as_result)
        else:
            print('Nothing was parsed')


html_parser = TestParser()

options = OptionParser()
options.add_option("--link", action='store', type='string', dest='parsing_link',
                  help="Provide page link should be parsed")

options, args = options.parse_args()

if options.parsing_link and options.parsing_link.startswith('http'):
    link = options.parsing_link
elif options.parsing_link:
    link = 'http://'+options.parsing_link
else:
    link = 'http://docs.python.org'


html_parser.parse(link)
