# coding:utf-8

from common import *

def split_text(text, limit):
    parts = []
    while len(text) > limit:
        part = text[:limit]
        last_newline_pos = part.rfind('\n')
        if last_newline_pos >= 0:
            part = part[:last_newline_pos]
        parts.append(part)
        text = text[len(part) + 1:]  # +1 to skip the newline
    parts.append(text)
    return parts


def handle(text):
    # 你的handle函数，这里只是一个示例
    prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L1
    result = get_data(text, prompt, model='gpt-3.5-turbo')  # gpt-3.5-turbo-16k
    return result


def merge_results(results):
    merged = {}
    for result in results:
        for key, value in result.items():
            if value != "":
                merged[key] = value
    return merged


def long_text_extractor(text, limit=4000):
    results = []
    split_parts = split_text(text, limit)
    for part in split_parts:
        result = handle(part)
        results.append(result)

    merged = merge_results(results)
    print(merged)
    return merged


if __name__ == "__main__":
    text = "这里是你的长文本"  # 请将此处替换为你的长文本
