import re


def fuzzyfinder(user_input, collection, ignorCase=False):
    suggestions = []
    pattern = '.*?'.join(user_input)
    if ignorCase:
        pattern = pattern.upper()
    regex = re.compile(pattern)
    for item in collection:
        match = regex.search(item.upper() if ignorCase else item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]


if __name__ == '__main__':
    colles = """zero one tow succ TRUE FALSE AND OR NOT""".split()
    res = fuzzyfinder("s", colles, True)
    print(res)
    res = fuzzyfinder("s", colles, False)
    print(res)
