import sys

def my_is_ascii(s):
    for c in s:
        if ord(c) >= 128:
            return False
    return True

is_ascii = my_is_ascii

if sys.version_info > (3, 8):
    def is_ascii(s: str):
        s.isascii()

is_ascii("abc")