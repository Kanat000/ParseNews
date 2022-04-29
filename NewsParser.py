from datetime import datetime

from dbConnection import Sqlite
from config import dbName
from bs4 import BeautifulSoup
import requests as requests
from urllib.parse import urlparse
import dateparser


def nested_loop(incoming, paths, k):
    details = paths[k].split('|')
    if k == (len(paths) - 1):
        return incoming.find_next(details[0], {details[1]: details[2]})
    else:
        return nested_loop(incoming.find_next(details[0], {details[1]: details[2]}), paths, k + 1)


def select_all_elements_by_path(soup, path_text):
    path_arr = path_text.split('&')
    i = 0
    tag_parent = path_arr[i].split('|')[0]
    attr_parent = path_arr[i].split('|')[1]
    value_parent = path_arr[i].split('|')[2]
    parent_tag_arr = soup.find_all(tag_parent, {attr_parent: value_parent})

    result_arr = []
    path_arr.pop(0)
    for x in parent_tag_arr:
        if len(path_arr) != 0:
            result_arr.append(nested_loop(x, path_arr, 0))
        else:
            result_arr = parent_tag_arr

    return result_arr


class Parser:
    def __init__(self):
        self.db = Sqlite(dbName)

    def parse(self, url):
        if self.db.exists_resource(url):
            url_info = urlparse(url)
            base_url = url_info.scheme + '://' + url_info.netloc
            response = requests.get(url)

            soup = BeautifulSoup(response.text, 'lxml')
            resource = self.db.get_resource(url)

            link_path = resource[3]
            result_link_arr = select_all_elements_by_path(soup, link_path)
            result_content_arr = []
            result_title_arr = []
            result_date_arr = []
            for link_tag in result_link_arr:
                page_soup = BeautifulSoup(requests.get(str(base_url + '' + urlparse(link_tag['href']).path)).text,
                                          'lxml')
                content_path = resource[4]
                result_content_arr.append(select_all_elements_by_path(page_soup, content_path))
                title_path = resource[5]
                result_title_arr += select_all_elements_by_path(page_soup, title_path)
                date_path = resource[6]
                result_date_arr += select_all_elements_by_path(page_soup, date_path)

            for i in range(len(result_link_arr)):
                link = str(base_url + '' + urlparse(result_link_arr[i]['href']).path)
                if not self.db.exists_item(link):
                    res_id = resource[0]
                    title = result_title_arr[i].text
                    content = ''
                    for content_elem in result_content_arr[i]:
                        content += content_elem.text
                    nd_date = dateparser.parse(result_date_arr[i].text).timestamp()
                    s_date = datetime.now().timestamp()
                    not_date = dateparser.parse(result_date_arr[i].text).date()
                    self.db.insert_items(res_id, link, title, content, nd_date, s_date, not_date)

            print(f"\nParsing successfully for URL('{url}')!!! Please check the items table!!!")
        else:
            print(f"\nResource('{url}') not exists in the database!!! Please, firstly insert resource in database!!!")

    def close(self):
        self.db.close()