#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint
import sys
import argparse

from http_filter.query.parser import QueryParser
from http_filter.query.lexer import QueryLexer
from http_filter.source import Source


def main(args=None):
    parser = argparse.ArgumentParser(description="HTTP Request filter tool")
    parser.add_argument("query", help="Query enclosed in \'\'")
    parser.add_argument("-i", dest="INPUT_FILE", help="input file (without it reads from STDIN)")
    parser.add_argument("-o", dest="OUTPUT_FILE", help="output file (witout it writes to STDOUT)")
    a = parser.parse_args()
    print(a.query)
    query_parser = QueryParser(QueryLexer(Source(a.query)))
    query_parser.parse()
    pp = pprint.PrettyPrinter(indent=4, width=1)
    print(query_parser.fields)
    pp.pprint(query_parser.ast)



if __name__ == "__main__":
    main()
