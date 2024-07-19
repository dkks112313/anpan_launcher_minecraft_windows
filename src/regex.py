# -*- coding: utf-8 -*-
import re


def check_to_latin_alphabet(string_match):
    regex = re.compile(r'^[a-zA-Z0-9_]+$')
    return bool(regex.match(string_match))
