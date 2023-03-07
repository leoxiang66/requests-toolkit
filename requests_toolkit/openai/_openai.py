# source: https://platform.openai.com/docs/api-reference/introduction
from pprint import pprint
import requests
from typing import Union, List, Awaitable
import aiohttp
import asyncio
from .config import ChatCompletionConfig


class ChatGPT:
    def __init__(self, api_key:str, model:str='gpt-3.5-turbo', global_system:str= ''):
        '''

        :param api_key: your openai api key
        :param model: model name
        :param global_system: The local_system message helps set the behavior of the assistant. In the example above, the assistant was instructed with “You are a helpful assistant.”
        '''
        self.model = model
        self.global_system = global_system
        # self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(api_key)
        }
        self.knowledge_base= dict()

    def print_KB(self):
        pprint(self.knowledge_base)

    def __update_KB__(self, key:str, value:str):
        if key not in self.knowledge_base:
            self.knowledge_base[key] = [value]
        else:
            self.knowledge_base[key].append(value)


    def __render_KB__(self,user_name:str):
        if user_name in self.knowledge_base:
            return ', '.join(self.knowledge_base[user_name])
        else:
            return ''
    def __build_headers_data__(self,param:ChatCompletionConfig):
        # 设置请求头和参数
        headers = self.headers
        user_msg = param.user_msg
        local_system = param.local_system
        assistant = param.assistant
        temperature = param.temparature
        top_p = param.top_p
        n = param.n
        stream = param.stream
        stop = param.stop
        max_tokens = param.max_tokens
        presence_penalty = param.presence_penalty
        frequency_penalty = param.frequency_penalty
        user_name = param.user_name

        data = dict(
            model=self.model,
            messages=[
                {'role': 'system', 'content': self.global_system if local_system is None else local_system},
                {"role": "user", "content": user_msg},
                {'role': "assistant", 'content': assistant if assistant is not None else self.__render_KB__(param.user_name)}
            ],
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            stop=stop,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            user=user_name
        )
        return dict(
            headers = headers,
            data = data
        )

    def reply(self,
                param: ChatCompletionConfig,
              ) ->Union[List[str], Awaitable]:

        # 1. build headers and data
        _  = self.__build_headers_data__(param)
        headers = _['headers']
        data = _['data']

        # 2. update knowledge base
        self.__update_KB__(param.user_name,param.user_msg)

        # 3. return request
        return self.__request__(headers,data,param.only_response)

    def __request__(self,headers, data, only_response):
        raise NotImplementedError()


class SyncChatGPT(ChatGPT):

    def __request__(self, headers, data,only_response):
        # 发送请求
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

        # 处理响应
        if response.status_code == 200:
            result = response.json()
            if only_response:
                tmp = result['choices']
                return [i['message']['content'] for i in tmp]

            return result
        else:
            raise IOError(response.json())


class AsyncChatGPT(ChatGPT):

    def __request__(self, headers, data, only_response,jupyter = False):
        async def request(headers,data,only_response):
            url = 'https://api.openai.com/v1/chat/completions'
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if only_response:
                            tmp = result['choices']
                            return [i['message']['content'] for i in tmp]
                        return result
                    else:
                        raise IOError(response.json())
        if jupyter:
            return request(headers,data,only_response)
        return asyncio.run(request(headers,data,only_response))



    def multi_reply(self,
                            params: List[ChatCompletionConfig],
                            jupyter = False
                          ):
        async def reply(param:ChatCompletionConfig):
            _ = self.__build_headers_data__(param)
            headers = _['headers']
            data = _['data']

            self.__update_KB__(param.user_name,param.user_msg)

            url = 'https://api.openai.com/v1/chat/completions'
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()

                        if param.only_response:
                            tmp = result['choices']
                            return [i['message']['content'] for i in tmp]
                        return result
                    else:
                        raise IOError(response.json())

        async def request(params):
            return await asyncio.gather(*tuple(reply(param) for param in params))

        if jupyter:
            return request(params)
        return asyncio.run(request(params))





