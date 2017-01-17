'''
Parser to get all last offers from
OLX.UA
OOP
'''

import time
import requests
import lxml.html

class OlxParser:

    def __init__(self, base_url):
        self.base_url = base_url
        self.last_time = ''

    def get_page(self):

        try:
            res = requests.get(self.base_url)
        except requests.ConnectionError:
            return

        if res.status_code < 400:
            return res.content

    def get_last_offer(self, html):
        html_tree = lxml.html.fromstring(html)
        path = ".//table[@id='offers_table']//td[@class='offer ']"

        # if there is no list of elements in our HTML_TREE, the code must be safe,
        # or if the returned object (LAST_OFFER.XPATH) has attribute "None":
        try:
            last_offer = html_tree.xpath(path)[0]
            link = last_offer.xpath(".//a")[1].get('href')
            time_node = last_offer.xpath('./table/tbody/tr[2]//p/text()')[2]
            cur_time = time_node.strip()[-5:]
        except (IndexError, AttributeError):
            return

        if self.last_time != cur_time:

            self.last_time = cur_time
            print(cur_time, link)

    def run(self):

        while True:
            #print('.')
            page = self.get_page()

            if page is None:
                time.sleep(0.5) # determine the interval of requests
                continue
            self.get_last_offer(page)

            time.sleep(0.5) # determine the interval of requests

if __name__ == "__main__":

    parser = OlxParser('https://www.olx.ua/list/')

    parser.run()
