# -*- coding: utf-8 -*-
# @Time : 2024/9/22 21:12
# @Author : xuxinhui
# @Email : xinhxu0720@163.com
# @File : UserContext.py.py
# @Project : 机器人
import contextvars

from openai import OpenAI

_my_context = contextvars.ContextVar('my_context', default=None)


def set_context_data(data):
    token = _my_context.set(data)
    # 通常在异步函数中，你需要保存这个token并在适当的时候使用它来重置上下文
    # 但在这个示例中，我们不会这么做


def get_context_data():
    return _my_context.get()

# 注意：在异步环境中，你应该在异步函数中使用这些函数，并可能需要管理token
# 这里仅为演示

# 在异步函数中使用
# async def some_async_function():
#     set_context_data({'key': 'value'})
#     # 执行一些操作
#     print(get_context_data())
#     # 可能需要重置上下文（如果有的话）

# 但在同步环境中，你通常不需要这样做，除非你有特殊需求


if __name__ == '__main__':
    set_context_data({'name':'1','age':'22'})
    print(get_context_data()['name'])


    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )