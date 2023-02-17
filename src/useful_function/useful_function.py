import re
import itertools


def unquote(encoded):
    return re.sub(r'\\u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: chr(int(m.group(1), 16)), encoded)


def quote(decoded):
    arr = []
    for c in decoded:
        t = hex(ord(c))[2:].upper()
        if len(t) >= 4:
            arr.append(f"%u{t}")
        else:
            arr.append(f"%{t}")
    return "".join(arr)


def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain((first,), iterable)


def safe_get(xpath_list, get_value="value", alt_output=None):
    if len(xpath_list) == 0:
        return alt_output

    return xpath_list[0].get(get_value)


# 테스트 코드
if __name__ == "__main__":
    print(quote('왜안됌?'))
