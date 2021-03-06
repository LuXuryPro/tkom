#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.source import Source


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


def test_http_source_is_steam_start():
    test_source = Source("a")
    assert test_source.is_stream_start() == True
    test_source.next_char()
    assert test_source.is_stream_start() == False
    test_source.next_char()
    assert test_source.is_stream_start() == False


def test_http_source_is_steam_end():
    test_source = Source("a")
    assert test_source.is_stream_end() == False
    test_source.next_char()
    assert test_source.is_stream_end() == False
    test_source.next_char()
    assert test_source.is_stream_end() == True


def test_source_line_switch():
    test_source = Source("a\r\nb\r\nc")
    assert test_source.get_current_line() == 1
    assert test_source.get_current_line_pos() == 0
    test_source.next_char()
    assert test_source.get_current_line() == 1
    assert test_source.get_current_line_pos() == 1
    test_source.next_char()
    assert test_source.get_current_line() == 1
    assert test_source.get_current_line_pos() == 2
    test_source.next_char()
    assert test_source.get_current_line() == 1
    assert test_source.get_current_line_pos() == 3

    test_source.next_char()
    assert test_source.get_current_line() == 2
    assert test_source.get_current_line_pos() == 1
    test_source.next_char()
    assert test_source.get_current_line() == 2
    assert test_source.get_current_line_pos() == 2
    test_source.next_char()
    assert test_source.get_current_line() == 2
    assert test_source.get_current_line_pos() == 3

    test_source.prev_char()
    assert test_source.get_current_line() == 2
    assert test_source.get_current_line_pos() == 2
    test_source.prev_char()
    assert test_source.get_current_line() == 2
    assert test_source.get_current_line_pos() == 1
    test_source.prev_char()
    assert test_source.get_current_line() == 1
    assert test_source.get_current_line_pos() == 3
