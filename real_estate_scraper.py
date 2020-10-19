import requests
from bs4 import BeautifulSoup
from pandas import DataFrame


class RockSpringScraper:

    def fetch_rockspring_properties(self):
        try:
            r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",
                             headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
            content = r.content
            soup = BeautifulSoup(content, "html.parser")
            all_properties = soup.find_all('div', {"class": "propertyRow"})
            property_list = []
            for i in all_properties:
                properties = {"price": i.find("h4", {"class": "propPrice"}).text.strip(),
                              "address1": i.find_all("span", {"class": "propAddressCollapse"})[0].text,
                              "address2": i.find_all("span", {"class": "propAddressCollapse"})[1].text}
                try:
                    properties["beds"] = i.find("span", {"class":"infoBed"}).find("b").text
                except:
                    properties["beds"] = None
                property_list.append(properties)
        except Exception as e:
            print(e)
        properties_df = DataFrame(property_list)
        return properties_df
