#! /usr/bin/python3.10
# -*- coding: utf-8 -*-
"""
Mini-projet Vigénére : fonctions de chiffrement et de déchiffrement
@author: 
"""

from string import ascii_uppercase

# Type alias

TKey = tuple[int]

# Functions


def chiffrer(phrase: str, k: TKey) -> str:
    crypted = ""
    i = 0
    for char in phrase:
        if char in ascii_uppercase:
            crypted += ascii_uppercase[
                (ascii_uppercase.find(char) +
                 k[i % len(k)]) % len(ascii_uppercase)
            ]
            i += 1
        else:
            crypted += char
    return crypted


def dechiffrer(phrase: str, k: TKey) -> str:
    return chiffrer(phrase, tuple(-i for i in k))


if __name__ == '__main__':
    msg = 'IL ETAIT UNE FOIS'
    k = (4, 2, 3)
    crypt_0 = chiffrer(msg, k)
    print(crypt_0)
    print(dechiffrer(crypt_0, k))
