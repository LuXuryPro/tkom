#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.source import Source
from http_filter.query.lexer import QueryLexer
from http_filter.query.parser import QueryParser
import pprint
pp = pprint.PrettyPrinter(indent=4, width=1)


def test_query_parser_simple_query():
    source = Source("url if (url == \"google.com\") and")
    p = QueryParser(QueryLexer(source))
    p.parse()
    pp.pprint(p.ast)
