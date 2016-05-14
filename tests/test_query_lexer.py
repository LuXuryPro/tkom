#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from http_filter.query.lexer import QueryLexer, QueryLexerException
from http_filter.source import Source


def test_query_lexer_next_token():
    source = Source('method if host == "google.pl"')
    lexer = QueryLexer(source)
    assert lexer.next_token() == "method"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "if"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "host"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "=="
    assert lexer.next_token() == " "
    assert lexer.next_token() == "\""
    assert lexer.next_token() == "google.pl"
    assert lexer.next_token() == "\""
    assert lexer.next_token() == ""


def test_query_lexer_prev_token():
    source = Source('method if host == "google.pl"')
    lexer = QueryLexer(source)
    assert lexer.prev_token() == ""
    assert lexer.next_token() == "method"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "if"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "host"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "=="
    assert lexer.next_token() == " "
    assert lexer.next_token() == "\""
    assert lexer.next_token() == "google.pl"
    assert lexer.next_token() == "\""
    assert lexer.next_token() == ""
    assert lexer.prev_token() == "\""
    assert lexer.prev_token() == "google.pl"


def test_query_lexer_exceptions():
    source = Source('method if host = "google.pl"')
    lexer = QueryLexer(source)
    assert lexer.prev_token() == ""
    assert lexer.next_token() == "method"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "if"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "host"
    assert lexer.next_token() == " "
    with pytest.raises(QueryLexerException) as e:
        assert lexer.next_token() == "=="
    assert str(e.value) == "Expected = or ~ at 16 found ' '"


def test_query_lexer_exceptions_tilde():
    source = Source('method if host ~ "google.pl"')
    lexer = QueryLexer(source)
    assert lexer.prev_token() == ""
    assert lexer.next_token() == "method"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "if"
    assert lexer.next_token() == " "
    assert lexer.next_token() == "host"
    assert lexer.next_token() == " "
    with pytest.raises(QueryLexerException) as e:
        assert lexer.next_token() == "=="
    assert str(e.value) == "Unexpected ~ at 15"


def test_query_lexer_small_query():
    source = Source('method if')
    lexer = QueryLexer(source)
    assert lexer.next_token() == "method"
    assert lexer.next_token_no_space() == "if"


def test_query_lexer_no_space():
    source = Source('method if method==\"GET\"')
    lexer = QueryLexer(source)
    assert lexer.next_token() == "method"
    assert lexer.next_token_no_space() == "if"
    assert lexer.next_token_no_space() == "method"
    assert lexer.next_token_no_space() == "=="
    assert lexer.next_token_no_space() == "\""
    assert lexer.next_token_no_space() == "GET"
    assert lexer.next_token_no_space() == "\""
