#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from http_filter.http.lexer import HTTPLexer, HTTPLexerException
from http_filter.source import Source


def test_lexer_get_next_token():
    source = Source(("POST /plugins/phsys.php HTTP/1.1\r\n"
                     "Content-Type: application/x-www-form-urlencoded\r\n"))
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


def test_lexer_get_next_token_get_prev_token():
    source = Source("HTTP/1.1\r\n")
    lexer = HTTPLexer(source)
    assert lexer.next_token() == "HTTP"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "\r\n"

    assert lexer.prev_token() == "1"
    assert lexer.prev_token() == "."
    assert lexer.prev_token() == "1"
    assert lexer.prev_token() == "/"
    assert lexer.prev_token() == "HTTP"
    assert lexer.prev_token() == ""


def test_lexer_get_next_token_big_spaces():
    source = Source(("POST                 "
                     "/plugins/phsys.php                  HTTP/1.1 "
                     "\r\n"))
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
    assert lexer.next_token() == " "
    assert lexer.next_token() == "\r\n"


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
    with pytest.raises(HTTPLexerException) as e:
        assert lexer.next_token()
    assert str(e.value) == "Not expected \\n at 32"


def test_lexer_exceptions_second_cr():
    source = Source("POST /plugins/phsys.php HTTP/1.1\r")
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
    with pytest.raises(HTTPLexerException) as e:
        lexer.next_token()
    assert str(e.value) == "Expected \\n at 33 found "


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


def test_lexer_get_next_past_end_token_get_prev_token():
    source = Source("HTTP/1.1\r\n")
    lexer = HTTPLexer(source)
    assert lexer.next_token() == "HTTP"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "\r\n"

    # called 2 times
    assert lexer.next_token() == ""
    assert lexer.next_token() == ""

    assert lexer.prev_token() == "\r\n"
    assert lexer.prev_token() == "1"
    assert lexer.prev_token() == "."
    assert lexer.prev_token() == "1"
    assert lexer.prev_token() == "/"
    assert lexer.prev_token() == "HTTP"
    assert lexer.prev_token() == ""


def test_lexer_get_next_token_get_prev_past_start_token():
    source = Source("HTTP/1.1\r\n")
    lexer = HTTPLexer(source)
    # called 2 times
    assert lexer.prev_token() == ""
    assert lexer.prev_token() == ""
    assert lexer.next_token() == "HTTP"
    assert lexer.next_token() == "/"
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "."
    assert lexer.next_token() == "1"
    assert lexer.next_token() == "\r\n"

    assert lexer.next_token() == ""
    assert lexer.next_token() == ""

    assert lexer.prev_token() == "\r\n"
    assert lexer.prev_token() == "1"
    assert lexer.prev_token() == "."
    assert lexer.prev_token() == "1"
    assert lexer.prev_token() == "/"
    assert lexer.prev_token() == "HTTP"
    assert lexer.prev_token() == ""


def test_lexer_exception_ends_with_free_text():
    source = Source("HTTP HTTP")
    lexer = HTTPLexer(source)
    assert lexer.prev_token() == ""
    assert lexer.next_token() == "HTTP"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "HTTP"
    assert lexer.next_token() == ""
    assert lexer.prev_token() == "HTTP"
    assert lexer.prev_token() == " "
    assert lexer.prev_token() == "HTTP"
    assert lexer.prev_token() == ""
