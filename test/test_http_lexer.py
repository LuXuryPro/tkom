#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_lexer import HTTPLexer
from source import Source


def test_lexer_get_next_token():
    source = Source("POST /plugins/phsys.php HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\n")
    lexer = HTTPLexer(source)
    assert lexer.prev_token() == ""
    assert lexer.next_token() == "POST"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "plugins"
    assert lexer.prev_token() == "/"
