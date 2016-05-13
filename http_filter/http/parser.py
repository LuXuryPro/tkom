#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.http.lexer import HTTPLexer

class HTTPParserException(Exception):
    pass

class HTTPParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.ast = {}
        self.ast["URL"] = []

    def parse(self):
        self._parse_status()
        

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
        slash = self.lexer.next_token_no_space()
        if slash != "/":
            message = self.lexer.exception_message("/", slash)
            raise HTTPParserException(message)
        self.ast["URL"].append("/")
        
        string = self.lexer.next_token()
        if string == " ":
            self.lexer.prev_token()
            return
        self.ast["URL"].append(string)
        while True:
            string = self.lexer.next_token()
            if string not in ["/", " ", "\r\n"]:
                self.ast["URL"].append(string)
            else:
                if string == " ":
                    return
                self.lexer.prev_token()
                break
        self._parse_url()


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
        self.ast["Version"] = {}
        self.ast["Version"]["Major"] = digit

        dot = self.lexer.next_token()
        if dot != ".":
            message = self.lexer.exception_message(".", dot)
            raise HTTPParserException(message)

        digit = self.lexer.next_token()
        if not digit.isdigit():
            message = self.lexer.exception_message("0-9", digit)
            raise HTTPParserException(message)
        self.ast["Version"]["Minor"] = digit
