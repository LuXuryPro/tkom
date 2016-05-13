#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.query.lexer import QueryLexer


class QueryParserException(Exception):
    pass


class QueryParser:
    def __init__(self, lexer: QueryLexer) -> None:
        self.lexer = lexer
        self.ast = {}

    def parse(self):
        self._parse_fields()
        token = self.lexer.next_token()
        if token != "if":
            message = self.lexer.exception_message("if", token)
            raise QueryParserException(message)
        self._parse_expression()

    def _parse_fields(self):
        self.ast["Fields"] = []
        while True:
            token = self.lexer.next_token_no_space()
            if token == "if":
                self.lexer.prev_token()
                break
            self.ast["Fields"].append(token)
            maybe_comma = self.lexer.next_token_no_space()
            if maybe_comma != ",":
                self.lexer.prev_token()
                break

    def _parse_expression(self):
        self._parse_term()
        token = self.lexer.next_token_no_space()
        while True:
            if token != "or":
                self.lexer.prev_token()
                return
            and_expr = {"o": "or", "left": self.ast}
            self._parse_factor()
            and_expr["right"] = self.ast
            self.ast = and_expr
            token = self.lexer.next_token_no_space()

    def _parse_term(self):
        self._parse_factor()
        token = self.lexer.next_token_no_space()
        while True:
            if token != "and":
                self.lexer.prev_token()
                return
            and_expr = {"o": "and", "left": self.ast}
            self._parse_factor()
            and_expr["right"] = self.ast
            self.ast = and_expr
            token = self.lexer.next_token_no_space()

    def _parse_factor(self):
        token = self.lexer.next_token_no_space()
        if token not in ["not", "("]:
            key = token
            operator = self.lexer.next_token_no_space()
            left_quote = self.lexer.next_token_no_space()
            value = self.lexer.next_token()
            right_quote = self.lexer.next_token()

            self.ast = {"t": "e", "k": key, "o": operator, "v": value}
        elif token == "not":
            self._parse_factor()
            not_expr = {"o": "not", "child": self.ast}
            self.ast = not_expr
        elif token == "(":
            self._parse_expression()
            token = self.lexer.next_token_no_space()
            if token != ")":
                message = self.lexer.exception_message(")", token)
                raise QueryParserException(message)
