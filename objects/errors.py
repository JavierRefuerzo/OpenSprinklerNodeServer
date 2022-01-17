#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""


class Errors :
    text: str = "Unknown Error"
    code: int = 500

    def __init__(self, text: str, code: int = 500):
        self.text = text
        self.code = code