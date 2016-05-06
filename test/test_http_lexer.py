#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from http_lexer import HTTPLexer,HTTPLexerException
from source import Source
import pdb


def test_lexer_get_next_token():
    source = Source("POST /plugins/phsys.php HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\n")
    lexer = HTTPLexer(source)
    assert lexer.next_token() == "POST"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "plugins"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "phsys"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "php"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "HTTP"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "1"

def test_lexer_get_next_token_big_spaces():
    source = Source("POST                 /plugins/phsys.php                  HTTP/1.1                         \r\n")
    lexer = HTTPLexer(source)
    assert lexer.next_token() == "POST"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "plugins"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "phsys"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "php"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "HTTP"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "1"

def test_lexer_exceptions():
    source = Source("POST /plugins/phsys.php HTTP/1.1\n\n")
    lexer = HTTPLexer(source)
    assert lexer.next_token() == "POST"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "plugins"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "phsys"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "php"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "HTTP"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "1"
    with pytest.raises(HTTPLexerException):
        assert lexer.next_token()

def test_lexer_exceptions_second():
    source = Source("n\n")
    lexer = HTTPLexer(source)
    assert lexer.next_token() == "n"
    with pytest.raises(HTTPLexerException):
        assert lexer.next_token()

def test_lexer_exception_empty_next():
    source = Source("")
    lexer = HTTPLexer(source)
    assert lexer.next_token() == ""
    assert lexer.next_token() == ""

def test_lexer_exception_empty_second():
    source = Source("")
    lexer = HTTPLexer(source)
    assert lexer.prev_token() == ""
    assert lexer.prev_token() == ""
