#!/usr/bin/env python
# -*- coding: utf-8 -*-

from source import Source

def test_http_source_constructor_has_one_argument():
    http_source = Source("GET / HTTP 1.1")

def test_http_source_constructor_argument_is_optional():
    http_source = Source()

def test_http_source_next_char_prev_char():
    test_source = Source("12345")
    assert test_source.next_char() == "1"
    assert test_source.prev_char() == ""
    assert test_source.next_char() == "1"
    assert test_source.next_char() == "2"
    assert test_source.prev_char() == "1"
    assert test_source.next_char() == "2"
    assert test_source.next_char() == "3"
    assert test_source.next_char() == "4"
    assert test_source.next_char() == "5"
    assert test_source.next_char() == ""
    assert test_source.prev_char() == "5"

def test_http_source_empty():
    test_source = Source("")
    assert test_source.next_char() == ""
    assert test_source.next_char() == ""
    assert test_source.prev_char() == ""
    assert test_source.prev_char() == ""

def test_http_source_empty_implicit():
    test_source = Source()
    assert test_source.next_char() == ""
    assert test_source.next_char() == ""
    assert test_source.prev_char() == ""
    assert test_source.prev_char() == ""

