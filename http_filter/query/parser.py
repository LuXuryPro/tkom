#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.query.lexer import QueryLexer


class QueryParserException(Exception):
    pass


class QueryParser:
    def __init__(self, lexer: QueryLexer) -> None:
        self.lexer = lexer
        self.ast = {}
        self.fields = []

    def parse(self):
        if self._parse_fields():
            token = self.lexer.next_token()
            if token != "if":
                message = self.lexer.exception_message("if", token)
                raise QueryParserException(message)
            self._parse_expression()
            token = self.lexer.next_token_no_space()

    def _parse_fields(self):
        while True:
            token = self.lexer.next_token_no_space()
            if token == "":
                return False
            if token == "if":
                self.lexer.prev_token()
                break
            elif token == ",":
                # empty comma
                message = self.lexer.exception_message("string", token)
                raise QueryParserException(message)

            self.fields.append(token)
            maybe_comma = self.lexer.next_token_no_space()
            if maybe_comma != ",":
                self.lexer.prev_token()
                break
        return True

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
        if token not in ["not", "(", ""]:
            key = token
            operator = self.lexer.next_token_no_space()
            if operator not in ["==", "=~"]:
                message = self.lexer.exception_message("== or =~", operator)
                raise QueryParserException(message)
            left_quote = self.lexer.next_token_no_space()
            if left_quote != "\"":
                message = self.lexer.exception_message("\"", left_quote)
                raise QueryParserException(message)
            value = self.lexer.next_token()
            right_quote = self.lexer.next_token()
            if right_quote != "\"":
                message = self.lexer.exception_message("\"", right_quote)
                raise QueryParserException(message)

            self.ast = {"k": key, "f": operator, "v": value}
        elif token == "not":
            self._parse_factor()
            not_expr = {"o": "not", "child": self.ast}
            self.ast = not_expr
        elif token == "(":
            self._parse_expression()
            token = self.lexer.next_token_no_space()
            if token != ")":
                message = self.lexer.exception_message(")", token)
                message += "\n"
                message += self.lexer.source.point_on_error()
                raise QueryParserException(message)
        elif token == "":
            return
