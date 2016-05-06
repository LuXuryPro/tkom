#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from query_lexer import QueryLexer, QueryLexerException
from source import Source


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
