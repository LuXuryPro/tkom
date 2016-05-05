#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from http_lexer import HTTPLexer,HTTPLexerException
from source import Source


def test_lexer_get_next_token():
    source = Source("POST /plugins/phsys.php HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\n")
    lexer = HTTPLexer(source)
    assert lexer.prev_token() == ""
    assert lexer.next_token() == "POST"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "plugins"
    assert lexer.prev_token() == "/"

def test_lexer_exceptions():
    source = Source("POST /plugins/phsys.php HTTP/1.1\n")
    lexer = HTTPLexer(source)
    assert lexer.next_token() == "POST"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "plugins"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "phsys"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "php"
    assert lexer.next_token() == "HTTP"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "1"
    with pytest.raises(HTTPLexerException):
        assert lexer.next_token()
