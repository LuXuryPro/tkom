#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse

from http_filter.http.lexer import HTTPLexer
from http_filter.http.parser import HTTPParser
from http_filter.query.parser import QueryParser
from http_filter.query.lexer import QueryLexer
from http_filter.query.matcher import Matcher
from http_filter.source import Source


def do_filtering(file, query_parser):
    packet = []
    for line in file.readlines():
        line = line.strip()
        if line == "=====":
            source_string = "".join(packet)
            http_parser = HTTPParser(HTTPLexer(Source(source_string)))
            http_parser.parse()
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
    except Exception as e:
        print(str(e))
        return
    if a.OUTPUT_FILE:
        sys.stdout = open(a.OUTPUT_FILE, "a")
    if a.INPUT_FILE:
        with open(a.INPUT_FILE) as f:
            do_filtering(f, query_parser)
    else:
        do_filtering(sys.stdin, query_parser)


if __name__ == "__main__":
    main()
