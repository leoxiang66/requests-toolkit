import requests
from typing import List, Union
import xmltodict
from pathlib import Path
import json
class BaseQuery:
    # class atributes
    if __name__ == '__main__':
        PACKAGE_ROOT = '.'
    else:
        PACKAGE_ROOT = str(Path(__package__).absolute())


    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    }
    @classmethod
    def __build_params__(cls, *args,**kwargs):
        raise NotImplemented

    @classmethod
    def __query__(cls, url:str, params:dict):
        '''

        :param url:
        :param params:
        :return: list of dicts, each dict contains info of a paper
        '''
        response = requests.get(url=url,params=params,headers=cls.HEADERS)
        return response

class PaperWithCodeQuery(BaseQuery):
    ENDPOINT = 'https://paperswithcode.com/api/v1/papers/'

    @classmethod
    def __build_params__(cls,query: str,
        page = 1,
        items_per_page = 50
        ):

        return {
            'page': page,
            'items_per_page': items_per_page,
            'title': query
        }

    @classmethod
    def __query__(cls, url: str, params: dict):
        return super().__query__(url, params)

    @classmethod
    def query(cls, query: str, page = 1, items_per_page = 50):
        params =  cls.__build_params__(query,page,items_per_page)
        return cls.__query__(cls.ENDPOINT, params).json()['results']


class ArxivQuery(BaseQuery):
    ENDPOINT = 'http://export.arxiv.org/api/query?'
    '''
    an example request:
    'http://export.arxiv.org/api/query?search_query=bert&max_results=1'
    '''
    @classmethod
    def __build_params__(cls,
                         query: str,
                         id_list: str = '',
                         start: int = 0,
                         max_results: int = 50
                         ):

        return {
            'search_query': query,
            'id_list': id_list,
            'start': start,
            'max_results': max_results
        }

    @classmethod
    def query(cls,
              query: str,
              id_list: str= '',
              start: int = 0,
              max_results: int = 50
              ) -> Union[dict, List[dict]]:
        params = cls.__build_params__(query,id_list,start,max_results)
        xml = cls.__query__(cls.ENDPOINT,params).content
        tmp = xmltodict.parse(xml)
        return tmp['feed']['entry']


class IEEEQuery(BaseQuery):
    '''
    an example query url:
    https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey={API_KEY}&querytext=BERT
    '''

    '''
    README:
    Please make sure a .config.json file is stored under the package root
    A template would be like this:
    {
        "api_key": "my api key"
    }
    '''
    ENDPOINT = 'https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey='

    @classmethod
    def __build_params__(cls, query: str):
        return {
            'querytext': query
        }

    @classmethod
    def query(cls, query: str) -> Union[dict, List[dict]]:
        with open(f"{cls.PACKAGE_ROOT}/.config.json", 'r', encoding='UTF-8') as f:
            api_key = json.load(f)['api_key']
        endpoint = cls.ENDPOINT + api_key + '&'
        params = cls.__build_params__(query)
        papers = cls.__query__(endpoint,params).json()['articles']
        return papers





if __name__ == '__main__':
    print(PaperWithCodeQuery.query('hello')[0])
    print(ArxivQuery.query('bert',max_results=1))
    # print(requests.get(url='http://export.arxiv.org/api/query?search_query=bert&max_results=1').content)
    print(IEEEQuery.query('bert')[0])

