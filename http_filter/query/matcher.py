#!/usr/bin/env python
# -*- coding: utf-8 -*-
from http_filter.http.parser import HTTPParser
from http_filter.query.parser import QueryParser


class Matcher:
    def __init__(self, http_packet: HTTPParser, query: QueryParser):
        self.httpPacket = http_packet
        self.query = query

    def matches(self) -> bool:
        if self.query.ast:
            return self.match_tree(self.query.ast)
        return True

    def match_tree(self, root) -> bool:
        if "o" in root:
            if root["o"] == "not":
                return not self.match_tree(root["child"])
            elif root["o"] == "or":
                return self.match_tree(root["left"]) or self.match_tree(
                    root["right"])
            elif root["o"] == "and":
                return self.match_tree(root["left"]) and self.match_tree(
                    root["right"])
        else:
            key = root["k"]
            val = root["v"]
            operation = root["f"]
            return self.match_packet(key, val, operation)

    def match_packet(self, key, val, function) -> bool:
        if not (key in self.httpPacket):
            return False
        if function == "==":
            if type(self.httpPacket[key.lower()]) is str:
                return self.httpPacket[key.lower()] == val
            else:
                return "".join(self.httpPacket[key.lower()]) == val
        if function == "=~":
            if type(self.httpPacket[key.lower()]) is str:
                return val in self.httpPacket[key.lower()]
            else:
                return val in "".join(self.httpPacket[key.lower()])
