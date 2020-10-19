from bs4 import BeautifulSoup
import requests
from pandas import DataFrame


class ProgrammablewebSpider:

    def get_api_details(self):
        headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        url = 'https://www.programmableweb.com/category/tools/api'
        base_url = 'https://www.programmableweb.com'
        rows = []
        response = requests.get(url=url, headers=headers)
        content = response.content
        while True:
            soup = BeautifulSoup(content, "html.parser")
            table = soup.find('table', {"class": "views-table cols-5 table"})
            if not table:
                return None
            page_rows = table.find_all('tr')
            del page_rows[0]
            rows.extend(page_rows)
            next_page_btn = soup.find('li', {'class': 'pager-next'})
            next_page = None
            if next_page_btn and next_page_btn.find('a') and not next_page_btn.find('a')['href'] is None:
                next_page = next_page_btn.find('a')['href']
            if next_page:
                url = base_url + next_page
                content = requests.get(url=url, headers=headers).content
            else:
                break
        apis = []
        for row in rows:
            category_col = row.find("td", {"class": "views-field views-field-field-article-primary-category"}).find(
                'a')
            api_detail = {"API Name": row.find("td", {"class": "views-field views-field-title"}).find('a').text.strip(),
                          "API Category": category_col.text,
                          "API URL": category_col['href'],
                          "API Description": row.find("td", {"class": "views-field views-field-field-api-description"}).text}
            apis.append(api_detail)
        apis_df = DataFrame(apis)

        return apis_df
