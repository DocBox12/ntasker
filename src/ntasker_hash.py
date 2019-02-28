#!/usr/bin/env python3

import hashlib

def hash(word):

    word_utf8 = word.encode("utf-8")
    value = hashlib.sha256()
    value.update(word_utf8)
    word_hash = value.hexdigest()
    return word_hash

