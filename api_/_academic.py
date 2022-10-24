import requests
from typing import List
class BaseQuery:
    # class atributes
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    }
    @classmethod
    def __build_params__(cls, *args,**kwargs):
        raise NotImplemented

    @classmethod
    def __query__(cls, url:str, params:dict) -> List[dict]:
        '''

        :param url:
        :param params:
        :return: list of dicts, each dict contains info of a paper
        '''
        results = requests.get(url=url,params=params,headers=cls.HEADERS).json()['results']
        return results

class PaperWithCodeQuery(BaseQuery):
    URL = 'https://paperswithcode.com/api/v1/papers/'

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
        return cls.__query__(cls.URL,params)


if __name__ == '__main__':
    print(PaperWithCodeQuery.query('hello')[0])

