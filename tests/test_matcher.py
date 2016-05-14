#!/usr/bin/env python
# -*- coding: utf-8 -*-
from http_filter.http.lexer import HTTPLexer
from http_filter.http.parser import HTTPParser
from http_filter.query.lexer import QueryLexer
from http_filter.query.matcher import Matcher
from http_filter.query.parser import QueryParser
from http_filter.source import Source


def test_matcher_query_one():
    source = "GET / HTTP/1.1\r\na:b\r\n\r\n"
    http_parser = HTTPParser(HTTPLexer(Source(source)))
    http_parser.parse()

    query = "method if method==\"GET\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if a==\"b\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if a==\"c\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == False

    query = "if a==\"c\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == False

    query = "if a==\"b\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True


def test_matcher_complex_sentence():
    source = "GET / HTTP/1.1\r\na:b\r\nc:d\r\n\r\n"
    http_parser = HTTPParser(HTTPLexer(Source(source)))
    http_parser.parse()

    query = "method if method==\"GET\" and c==\"d\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if (method==\"GET\" and c==\"d\")"
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if (method==\"GET\" and a==\"b\" and c==\"d\")"
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if not (method==\"GET\" and a==\"b\" and c==\"d\")"
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == False

    query = "method if method==\"POST\" or a==\"b\" and c==\"d\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if (method==\"POST\" or a==\"b\") and c==\"d\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if (method==\"POST\" and a==\"b\") or c==\"d\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True


def test_matcher_special_operator():
    source = "GET / HTTP/1.1\r\na:asdf\r\nc:d\r\n\r\n"
    http_parser = HTTPParser(HTTPLexer(Source(source)))
    http_parser.parse()

    query = "method if method==\"GET\" and a=~\"a\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a=~\"s\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a=~\"d\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a=~\"f\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a=~\"as\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a=~\"sd\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a=~\"df\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a=~\"asd\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a=~\"sdf\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a=~\"asdf\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True

    query = "method if method==\"GET\" and a== \"asdf\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True


def test_matcher_empty_query():
    source = "GET / HTTP/1.1\r\na:asdf\r\nc:d\r\n\r\n"
    http_parser = HTTPParser(HTTPLexer(Source(source)))
    http_parser.parse()

    query = ""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == True


def test_matcher_unknown_key():
    source = "GET / HTTP/1.1\r\na:asdf\r\nc:d\r\n\r\n"
    http_parser = HTTPParser(HTTPLexer(Source(source)))
    http_parser.parse()

    query = "method if g==\"h\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == False

    query = "method if post==\"get\""
    query_parser = QueryParser(QueryLexer(Source(query)))
    query_parser.parse()
    matcher = Matcher(http_parser, query_parser)
    assert matcher.matches() == False
