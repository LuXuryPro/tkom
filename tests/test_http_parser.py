#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.source import Source
from http_filter.http.lexer import HTTPLexer
from http_filter.http.parser import HTTPParser


def test_http_parser_standard_packet():
    source = Source("GET /test.php//asd HTTP/0.9\r\n"
                    "a: b\r\n"
                    "c:d\r\n"
                    "\r\n")
    p = HTTPParser(HTTPLexer(source))
    p.parse()
    assert p.ast["method"] == "GET"
    assert p.ast["url"] == ['/', 'test', '.', 'php', '/', '/', 'asd']
    assert p.ast["signature"] == "HTTP"
    assert p.ast["version"]["major"] == "0"
    assert p.ast["version"]["minor"] == "9"
    assert p.ast["headers"][0]["key"] == "a"
    assert p.ast["headers"][0]["val"] == ["b"]
    assert p.ast["headers"][1]["key"] == "c"
    assert p.ast["headers"][1]["val"] == ["d"]
    assert p.ast["body"] == []


def test_http_parser_post_packet_with_body():
    source = Source("POST /test.php//asd HTTP/0.9\r\n"
                    "a: b\r\n"
                    "c:d\r\n"
                    "\r\n"
                    "body")
    p = HTTPParser(HTTPLexer(source))
    p.parse()
    assert p.ast["method"] == "POST"
    assert p.ast["url"] == ['/', 'test', '.', 'php', '/', '/', 'asd']
    assert p.ast["signature"] == "HTTP"
    assert p.ast["version"]["major"] == "0"
    assert p.ast["version"]["minor"] == "9"
    assert p.ast["headers"][0]["key"] == "a"
    assert p.ast["headers"][0]["val"] == ["b"]
    assert p.ast["headers"][1]["key"] == "c"
    assert p.ast["headers"][1]["val"] == ["d"]
    assert p.ast["body"] == ["body"]


def test_http_parser_whitespace_tolerance():
    source = Source("POST     /test.php//asd        HTTP/0.9   \r\n"
                    " a: b\r\n"
                    "c   :d \r\n"
                    "e   :  f\r\n    "
                    "\r\n"
                    "body")
    p = HTTPParser(HTTPLexer(source))
    p.parse()
    assert p.ast["method"] == "POST"
    assert p.ast["url"] == ['/', 'test', '.', 'php', '/', '/', 'asd']
    assert p.ast["signature"] == "HTTP"
    assert p.ast["version"]["major"] == "0"
    assert p.ast["version"]["minor"] == "9"
    assert p.ast["headers"][0]["key"] == "a"
    assert p.ast["headers"][0]["val"] == ["b"]
    assert p.ast["headers"][1]["key"] == "c"
    assert p.ast["headers"][1]["val"] == ["d", " "]
    assert p.ast["headers"][2]["key"] == "e"
    assert p.ast["headers"][2]["val"] == ["f"]
    assert p.ast["body"] == ["body"]


def test_http_parser_real_packet():
    source = Source(
        "GET /ajax/libs/jquery/1.7.1/jquery.min.js HTTP/1.1\r\n"
        "Host: ajax.googleapis.com\r\n"
        "Connection: keep-alive\r\n"
        "Cache-Control: max-age=0\r\n"
        "Accept: */*\r\n"
        "Accept-Encoding: gzip, deflate, sdch\r\n"
        "Accept-Language: pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4\r\n"
        "If-Modified-Since: Fri, 16 Oct 2015 18:27:31 GMT\r\n"
        "\r\n"
                    )
    p = HTTPParser(HTTPLexer(source))
    p.parse()
    print(p)
