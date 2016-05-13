#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.source import Source
from http_filter.http.lexer import HTTPLexer
from http_filter.http.parser import HTTPParser
import pytest


def test_http_parser_standard_packet():
    source = Source("GET /test.php//asd HTTP/0.9\r\n"
                    "a: b\r\n"
                    "c:d\r\n"
                    "\r\n")
    p = HTTPParser(HTTPLexer(source))
    p.parse()
    assert p.ast["Method"] == "GET"
    assert p.ast["URL"] == ['/', 'test', '.', 'php', '/', '/', 'asd']
    assert p.ast["signature"] == "HTTP"
    assert p.ast["Version"]["Major"] == "0"
    assert p.ast["Version"]["Minor"] == "9"
    assert p.ast["Headers"][0]["key"] == "a"
    assert p.ast["Headers"][0]["val"] == ["b"]
    assert p.ast["Headers"][1]["key"] == "c"
    assert p.ast["Headers"][1]["val"] == ["d"]
    assert p.ast["Body"] == []


def test_http_parser_post_packet_with_body():
    source = Source("POST /test.php//asd HTTP/0.9\r\n"
                    "a: b\r\n"
                    "c:d\r\n"
                    "\r\n"
                    "body")
    p = HTTPParser(HTTPLexer(source))
    p.parse()
    assert p.ast["Method"] == "POST"
    assert p.ast["URL"] == ['/', 'test', '.', 'php', '/', '/', 'asd']
    assert p.ast["signature"] == "HTTP"
    assert p.ast["Version"]["Major"] == "0"
    assert p.ast["Version"]["Minor"] == "9"
    assert p.ast["Headers"][0]["key"] == "a"
    assert p.ast["Headers"][0]["val"] == ["b"]
    assert p.ast["Headers"][1]["key"] == "c"
    assert p.ast["Headers"][1]["val"] == ["d"]
    assert p.ast["Body"] == ["body"]


def test_http_parser_whitespace_tolerance():
    source = Source("POST     /test.php//asd        HTTP/0.9   \r\n"
                    " a: b\r\n"
                    "c   :d \r\n"
                    "e   :  f\r\n    "
                    "\r\n"
                    "body")
    p = HTTPParser(HTTPLexer(source))
    p.parse()
    assert p.ast["Method"] == "POST"
    assert p.ast["URL"] == ['/', 'test', '.', 'php', '/', '/', 'asd']
    assert p.ast["signature"] == "HTTP"
    assert p.ast["Version"]["Major"] == "0"
    assert p.ast["Version"]["Minor"] == "9"
    assert p.ast["Headers"][0]["key"] == "a"
    assert p.ast["Headers"][0]["val"] == ["b"]
    assert p.ast["Headers"][1]["key"] == "c"
    assert p.ast["Headers"][1]["val"] == ["d", " "]
    assert p.ast["Headers"][2]["key"] == "e"
    assert p.ast["Headers"][2]["val"] == ["f"]
    assert p.ast["Body"] == ["body"]
