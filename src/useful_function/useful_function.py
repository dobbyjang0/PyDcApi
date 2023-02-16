import re
import itertools

def unquote(encoded):
    return re.sub(r'\\u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: chr(int(m.group(1), 16)), encoded)

def quote(decoded):
    arr = []
    for c in decoded:
        t = hex(ord(c))[2:].upper()
        if len(t) >= 4:
            arr.append("%u" + t)
        else:
            arr.append("%" + t)
    return "".join(arr)

def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain((first,), iterable)

#테스트 코드
if __name__ == "__main__":
    print(quote('왜안됌?'))