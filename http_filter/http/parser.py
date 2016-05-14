#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.http.lexer import HTTPLexer


class HTTPParserException(Exception):
    pass


class HTTPParser:
    def __init__(self, lexer: HTTPLexer):
        self.lexer = lexer
        self.ast = {}

    def parse(self):
        self._parse_status()
        self._parse_headers()
        self._parse_body()

    def _parse_status(self):
        method = self.lexer.next_token_no_space()
        if method in ["/", ".", ":"]:
            return False
        self.ast["method"] = method
        self._parse_url()
        self._parse_signature()
        crlf = self.lexer.next_token_no_space()
        if crlf != "\r\n":
            message = self.lexer.exception_message("\r\n", crlf)
            raise HTTPParserException(message)

    def _parse_url(self):
        self.ast["url"] = []
        while True:
            slash = self.lexer.next_token_no_space()
            if slash != "/":
                message = self.lexer.exception_message("/", slash)
                raise HTTPParserException(message)
            self.ast["url"].append("/")
            string = self.lexer.next_token()
            while True:
                if string not in ["/", " ", "\r\n"]:
                    self.ast["url"].append(string)
                else:
                    if string == " ":
                        return
                    self.lexer.prev_token()
                    break
                string = self.lexer.next_token()

    def _parse_signature(self):
        signature = self.lexer.next_token()
        if signature != "HTTP":
            message = self.lexer.exception_message("HTTP", signature)
            raise HTTPParserException(message)
        self.ast['signature'] = signature
        slash = self.lexer.next_token()
        if slash != "/":
            message = self.lexer.exception_message("slash", slash)
            raise HTTPParserException(message)
        self._parse_version()

    def _parse_version(self):
        digit = self.lexer.next_token()
        if not digit.isdigit():
            message = self.lexer.exception_message("0-9", digit)
            raise HTTPParserException(message)
        self.ast["version"] = {}
        self.ast["version"]["major"] = digit

        dot = self.lexer.next_token()
        if dot != ".":
            message = self.lexer.exception_message(".", dot)
            raise HTTPParserException(message)

        digit = self.lexer.next_token()
        if not digit.isdigit():
            message = self.lexer.exception_message("0-9", digit)
            raise HTTPParserException(message)
        self.ast["version"]["minor"] = digit

    def _parse_headers(self):
        self.ast["headers"] = []
        while True:
            crfl_end = self.lexer.next_token_no_space()
            if crfl_end == "\r\n":
                break
            elif crfl_end == "":
                message = self.lexer.exception_message("string or CRLF", "EOF")
                raise HTTPParserException(message)
            else:
                k = crfl_end
                separator = self.lexer.next_token_no_space()
                if separator != ":":
                    message = self.lexer.exception_message(":", separator)
                    raise HTTPParserException(message)
                v = []
                val = self.lexer.next_token_no_space()
                if val == "\r\n":
                    message = self.lexer.exception_message("string", val)
                    raise HTTPParserException(message)
                v.append(val)
                while True:
                    val = self.lexer.next_token()
                    if val == "\r\n":
                        self.ast["headers"].append(
                            {"key": k.lower(), "val": v})
                        break

                    v.append(val)

    def _parse_body(self):
        self.ast["body"] = []
        while True:
            token = self.lexer.next_token()
            if token == "":
                break
            self.ast["body"].append(token)

    def __getitem__(self, item: str) -> str:
        try:
            return self.ast[item.lower()]
        except:
            for header in self.ast["headers"]:
                if header["key"] == item.lower():
                    return header["val"]
        raise IndexError

    def __contains__(self, item) -> bool:
        try:
            return self.ast[item.lower()]
        except:
            for header in self.ast["headers"]:
                if header["key"] == item.lower():
                    return header["val"]
        return False

    def __str__(self):
        rep = "==HTTP Request==\n"
        rep += "Method: " + self.ast["method"] + "\n"
        rep += "URL: " + "".join(self.ast["url"]) + "\n"
        rep += "Version Major: " + self.ast["version"]["major"] + "\n"
        rep += "Version Minor: " + self.ast["version"]["minor"] + "\n"
        rep += "Headers:\n"
        for header in self.ast["headers"]:
            rep += "\t" + header["key"] + " = " + "".join(header["val"]) + "\n"
        if self.ast["body"]:
            rep += "body:\n"
            rep += "".join(self.ast["body"])
        return rep
