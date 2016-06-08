#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse

from http_filter.http.lexer import HTTPLexer, HTTPLexerException
from http_filter.http.parser import HTTPParser, HTTPParserException
from http_filter.query.parser import QueryParser, QueryParserException
from http_filter.query.lexer import QueryLexer, QueryLexerException
from http_filter.query.matcher import Matcher
from http_filter.source import Source


def do_filtering(file_stream, query_parser):
    packet = []
    for line in file_stream.readlines():
        line = line.strip()
        if line == "=====":
            source_string = "".join(packet)
            http_parser = HTTPParser(HTTPLexer(Source(source_string)))
            try:
                http_parser.parse()
            except HTTPLexerException as e:
                print("HTTP Lexer Exception:")
                print(str(e))
                return
            except HTTPParserException as e:
                print("HTTP Parser Exception:")
                print(str(e))
                return
            matcher = Matcher(http_parser, query_parser)
            if matcher.matches():
                print("##########")
                if query_parser.fields:
                    for field in query_parser.fields:
                        try:
                            val = http_parser[field]
                            print(field + " = " + val)
                        except:
                            continue
                else:
                    print(http_parser)
            packet = []
        else:
            packet.append(line + "\r\n")


def main(args=None):
    parser = argparse.ArgumentParser(description="HTTP Request filter tool")
    parser.add_argument("query", help="Query enclosed in \'\'")
    parser.add_argument("-i", dest="INPUT_FILE",
                        help="input file (without it reads from STDIN)")
    parser.add_argument("-o", dest="OUTPUT_FILE",
                        help="output file (witout it writes to STDOUT)")
    a = parser.parse_args()
    query_parser = QueryParser(QueryLexer(Source(a.query)))
    try:
        query_parser.parse()
    except QueryLexerException as e:
        print("Query Lexer Exception:")
        print(str(e))
        return
    except QueryParserException as e:
        print("Query Parser Exception:")
        print(str(e))
        return
    if a.OUTPUT_FILE:
        sys.stdout = open(a.OUTPUT_FILE, "a")
    if a.INPUT_FILE:
        try:
            with open(a.INPUT_FILE) as f:
                do_filtering(f, query_parser)
        except FileNotFoundError as e:
            print("File " + a.INPUT_FILE + " not found")
            sys.exit(-1)
    else:
        do_filtering(sys.stdin, query_parser)


if __name__ == "__main__":
    main()
