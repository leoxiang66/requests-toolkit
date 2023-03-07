# source: https://platform.openai.com/docs/api-reference/introduction
from pprint import pprint

import requests
from typing import Union, List, Awaitable
import aiohttp
import asyncio


class ChatCompletionConfig:
    def __init__(self,
        user_name: str,
        user_msg: str,
        assistant: str = None,
        local_system:str = None,
        temperature:float = 1,
        top_p:float = 1,
        n:int = 1,
        stream:bool = False,
        stop: Union[str, List[str]] = None,
        max_tokens:int = 1000,
        presence_penalty:float = 0,
        frequency_penalty:float = 0,
        only_response = True,
                 ):
        '''

         :param user_msg: user message
         :param assistant: external knowledge base. E.g. chat history
         :param temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the     output more random, while lower values like 0.2 will make it more focused and deterministic.
             We generally recommend altering this or top_p but not both.
         :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model         considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising    the top 10% probability mass are considered.
             We generally recommend altering this or temperature but not both.
         :param n: How many chat completion choices to generate for each input message.
         :param stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
         :param stop: Up to 4 sequences where the API will stop generating further tokens.
         :param max_tokens: The maximum number of tokens allowed for the generated answer. By default, the number of tokens the model can return will be (4096 - prompt tokens).
         :param presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
         :param frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
         :param user_name: A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.
         :param only_response: if only return the text response from ChatGPT

         :return:
         '''
        self.user_name = user_name
        self.user_msg = user_msg
        self.assistant = assistant
        self.local_system =  local_system
        self.temparature = temperature
        self.top_p = top_p
        self.n = n
        self.stream = stream
        self.stop = stop
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.only_response = only_response

    def to_dict(self) -> dict:
        ret = {}
        for key, value in self.__dict__.items():
            if hasattr(value, 'to_dict'):
                ret[key] = value.to_dict()
            else:
                ret[key] = value
        return ret



class ChatGPT:
    def __init__(self, api_key:str, async_: bool, model:str='gpt-3.5-turbo', global_system:str= ''):
        '''

        :param api_key: your openai api key
        :param async_: if the IO is asynchronized
        :param model: model name
        :param global_system: The local_system message helps set the behavior of the assistant. In the example above, the assistant was instructed with “You are a helpful assistant.”
        '''
        self.async_ = async_
        self.model = model
        self.global_system = global_system
        # self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(api_key)
        }
        self.knowledge_base= []

    def __build_KB__(self):
        return ', '.join(self.knowledge_base)

    def reply(self,
                param: ChatCompletionConfig
              ) ->Union[List[str], Awaitable]:

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
        only_response = param.only_response

        self.knowledge_base.append(user_msg)

        # 设置请求头和参数
        headers = self.headers

        data = dict(
            model= self.model,
            messages = [
                {'role': 'system', 'content': self.global_system if local_system is None else local_system},
                {"role": "user", "content": user_msg},
                {'role': "assistant", 'content':assistant if assistant is not None else self.__build_KB__()}
            ],
            temperature= temperature,
            top_p = top_p,
            n = n,
            stream = stream,
            stop = stop,
            max_tokens= max_tokens,
            presence_penalty = presence_penalty,
            frequency_penalty = frequency_penalty,
            user = user_name
        )
        return self.__request__(headers,data,only_response)

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

    async def __request__(self, headers, data, only_response):
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

    async def multi_reply(self,
                            params: List[ChatCompletionConfig]
                          ):
        return await asyncio.gather(*tuple(self.reply(param) for param in params))


if __name__ == '__main__':
    # chat = SyncChatGPT("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",False,global_system="You're my girl.")
    #
    param = ChatCompletionConfig(user_name='leo23', user_msg='hi')
    param2 = ChatCompletionConfig(user_name='leo26', user_msg='I hate you!')
    # a= chat.reply(param)
    #
    # print(a)
    b = AsyncChatGPT('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',True)
    # print(asyncio.run(b.reply(param)))
    print(asyncio.run(b.multi_reply([param,param2])))


