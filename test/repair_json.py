import re

import re
import json

import json


def repair_json(data):
    while True:
        try:
            # Try to load the string as a JSON
            json.loads(data)
            return data  # return if it is a valid JSON
        except json.JSONDecodeError:
            # If JSON is invalid, find the last valid opening mark and cut the string
            open_position = max(data.rfind("{"), data.rfind("["), data.rfind('"'))
            close_position = max(data.rfind("}"), data.rfind("]"), data.rfind('"'))

            # Check for unbalanced quotes
            quote_count = data.count('"')
            unbalanced_quotes = quote_count % 2 != 0

            left_bracket_count = data.count("[")
            right_bracket_count = data.count("]")
            unbalanced_brackets = left_bracket_count != right_bracket_count

            if open_position > close_position:
                if unbalanced_quotes and data[open_position] == '"':
                    # If last opening mark is a quote and quotes are unbalanced, add closing quote
                    data = data[:open_position + 1] + '"'
                else:
                    # If last opening mark is a bracket, remove it
                    data = data+']' if data[-1]=='[' else data[:open_position]
            else:
                if unbalanced_quotes and data[close_position] == '"':
                    # If last closing mark is a quote and quotes are unbalanced, remove it
                    data = data[:close_position]
                else:
                    # If last closing mark is a bracket, add corresponding closing bracket
                    # bracket = "}" if data[close_position] == "]" else "]"
                    bracket=""
                    if (data[close_position] == "]" or data[close_position] == '"') and not unbalanced_brackets:
                        bracket = "}"
                    elif unbalanced_brackets:
                        bracket = "]"

                    data = data[:close_position + 1] + bracket

            # If no valid opening mark found, assume the JSON string is too broken and return an empty dict
            if open_position == -1 and close_position == -1:
                return "{}"


data = """{"name":"tom", "articles":["i'm a boy","""
res = repair_json(data)
print(res)

data = """{"name":"tom", "articles":["i'm a bo"""
res = repair_json(data)
print(res)

data = """{"name":"tom", "articl"""
res = repair_json(data)
print(res)