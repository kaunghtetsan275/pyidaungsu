# The MIT License (MIT)
# Copyright (c) 2018 Thura Hlaing

import re
import json
import pkgutil
import itertools


def build_pattern(pattern, data):
    # build regular expression from a pattern
    if isinstance(pattern, str):
        node = pattern[:pattern.find('_')] if '_' in pattern else pattern
        or_expr = "|".join(
            [
                re.escape(x) for x in
                sorted(set(data[node].values()), key=len, reverse=True) if x
            ]
        )
        return '(?P<{}>{})'.format(pattern, or_expr)

    if isinstance(pattern, tuple):
        lst = [build_pattern(x, data) for x in pattern]
        if len(lst) > 1:
            or_expr = "|".join(lst)
            return '(%s){0,%d}' % (or_expr, len(lst))
        else:
            return '({})?'.format(lst[0])

    if isinstance(pattern, list):
        return ''.join([build_pattern(x, data) for x in pattern])


def build_table(data, reverse=False):
    # build conversion table from json mapping data.
    ret = {}
    for key, value in data.items():
        if reverse:
            ret.update({v: k for k, v in value.items() if v})
        else:
            ret.update({k: v for k, v in value.items() if v})
    return ret


class BaseEncoding():
    def __init__(self):
        # get json file name dynamically from class name
        encname = self.__class__.__name__
        filename = encname[:encname.find('Encoding')].lower() + '.json'
        self.json_data = json.loads(
            pkgutil.get_data('myanmar', 'data/' + filename).decode('utf-8')
        )

        self.table = build_table(self.json_data)
        self.reverse_table = build_table(self.json_data, reverse=True)

        pattern = "|".join(
            [
                build_pattern(x, self.json_data)
                for x in self._morphologic_pattern
            ]
        )
        self.morphologic_pattern = re.compile(
            "(?P<syllable>{})".format(pattern), re.UNICODE
        )

        # flattern syllable_pattern, convert to a list of tuples first
        syllable_parts = [
            (x, ) if isinstance(x, str) else x
            for x in self._morphologic_syllable
        ]
        self.syllable_parts = list(itertools.chain(*syllable_parts))

        if hasattr(self, '_phonemic_pattern'):
            pattern = "|".join(
                [
                    build_pattern(x, self.json_data)
                    for x in self._phonemic_pattern
                ]
            )
            self.phonemic_pattern = re.compile(
                "(?P<syllable>{})".format(pattern), re.UNICODE
            )


class UnicodeEncoding(BaseEncoding):
    def __init__(self, *args, **kwargs):
        self._morphologic_syllable = [
            ("kinzi", ),
            "consonant",
            ("stack", ),
            ("yapin", "yayit", "wasway", "hatoh"),
            ("eVowel", "iVowel"),
            ("uVowel", "anusvara", "aiVowel"),
            ("aaVowel", "asat"),
            ("dotBelow", "visarga"),
        ]
        self._morphologic_pattern = (
            "independent",
            "digit",
            "punctuation",
            "ligature",
            self._morphologic_syllable,
        )

        self._phonemic_syllable = [
            "consonant",
            ("yapin", "yayit", "wasway", "hatoh"),
            ("eVowel", "iVowel"),
            ("uVowel", "anusvara", "aiVowel"),
            ("aaVowel", "asat"),
            (["consonant_devowel", ("dotBelow_devowel", ), "asat_devowel"], ),
            ("dotBelow", "visarga"),
            (["consonant_stack", "virama_stack"], ),
        ]
        self._phonemic_pattern = (
            "independent",
            "digit",
            "punctuation",
            "ligature",
            self._phonemic_syllable,
        )
        super().__init__(*args, **kwargs)


class LegacyEncoding(BaseEncoding):
    def __init__(self, *args, **kwargs):
        self._morphologic_syllable = [
            ("eVowel", ), ("yayit", ), "consonant", ("kinzi", "stack"),
            ("yapin", "wasway", "hatoh"), ("iVowel", "uVowel", "anusvara"),
            ("aiVowel", ), ("aaVowel", "asat", "dotBelow"), ("visarga", )
        ]
        self._morphologic_pattern = (
            "independent", "digit", "punctuation", "ligature",
            self._morphologic_syllable
        )

        super().__init__(*args, **kwargs)


class ZawgyiEncoding(LegacyEncoding):
    pass


class WininnwaEncoding(LegacyEncoding):
    pass
