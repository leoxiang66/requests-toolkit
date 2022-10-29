from typing import List
import time
import json
import os
from lxml import etree
from tqdm import tqdm
import requests
class AirQualityQuery:
    KEY = '550b1b06-665d-41f5-b606-c26d06646a20'
    ENDPOINT = '''http://api.airvisual.com/v2/'''
    PATH = '.CITIES.json'
    HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
}

    if os.path.exists(PATH):
        with open(PATH, 'r', encoding='UTF-8') as f:
            CITIES = json.load(f)
    else:
        CITIES = dict()

    @classmethod
    def __get__provinces__(cls,country: str) -> List[str]:
        url = cls.ENDPOINT + 'states?'
        tmp = requests.get(url,dict(
            country=country,
            key=cls.KEY
        )).json()

        response_state = tmp['status']
        while response_state != 'success':
            time.sleep(10)
            tmp = requests.get(url, dict(
                country=country,
                key=cls.KEY
            )).json()
            response_state = tmp['status']
        provinces = [x['state'] for x in tmp['data']]
        return provinces

    @classmethod
    def __get__cities_in_province__(cls,province: str, country: str) -> List[str]:
        url = cls.ENDPOINT + 'cities?'
        tmp = requests.get(url,dict(
            state = province,
            key=cls.KEY,
            country = country
        )).json()

        response_state = tmp['status']
        while response_state != 'success':
            time.sleep(10)
            tmp = requests.get(url, dict(
                state=province,
                key=cls.KEY,
                country=country
            )).json()
            response_state = tmp['status']

        cities = [x['city'] for x in tmp['data']]
        return cities

    @classmethod
    def __get_cities_in_country__(cls,country:str) -> List[str]:
        if country not in cls.CITIES:
            cls.CITIES[country] = dict()
            provinces = cls.__get__provinces__(country)  # [str]
            for i in tqdm(range(len(provinces))):
                province = provinces[i]
                cities = cls.__get__cities_in_province__(province, country)
                cls.CITIES[country][province] = cities

            with open(cls.PATH,'w') as f:
                f.write(json.dumps(cls.CITIES))

        return cls.CITIES[country]

    @classmethod
    def air_quality_by_country(cls, country: str, return_frequency: int = None):
        if country not in cls.CITIES:
            data = cls.__get_cities_in_country__(country)
        else:
            data = cls.CITIES[country]

        url = f'''https://www.iqair.com/{country.lower()}'''

        aqi_values = []

        for prov, cities in data.items():
            for city in cities:
                html = requests.get(f'''{url}/{prov.lower()}/{city.lower()}''', headers=cls.HEADERS).text
                try:
                    aqi = int(etree.HTML(html).xpath('//p[@class="aqi-value__value"]//text()')[0])
                except:
                    continue
                aqi_values.append((city,prov, aqi))
                if return_frequency and len(aqi_values) % return_frequency ==0:
                    aqi_values.sort(key=lambda x: x[2])
                    yield aqi_values


        aqi_values.sort(key= lambda x: x[2])
        yield aqi_values


if __name__ == '__main__':
    # print(AirQualityQuery.__get__provinces__('china'))
    generator = AirQualityQuery.air_quality_by_country('china', 10)
    for i in generator:
        print(i)
        print()