#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.lexer import Lexer


class QueryLexerException(Exception):
    pass


class QueryLexer(Lexer):
    def _get_token(self) -> str:
        """
        private _get_token
        """
        c = self.source.next_char()
        # go throught all spaces and return only one
        if c == " ":
            while c == " ":
                c = self.source.next_char()

            self.source.prev_char()
            return " "
        # one char tokens can be returned immediately
        if c in [",", "(", ")", "\""]:
            return c
        if c == "~":
            raise QueryLexerException("Unexpected ~ at {pos}".format(
                pos=self.source.get_current_position()))
        if c == "=":
            n = self.source.next_char()
            if n in ["=", "~"]:
                return c + n
            else:
                raise QueryLexerException(
                        "Expected = or ~ at {pos} found '{c}'".format(
                        pos=self.source.get_current_position(
                        ), c=n))

        # collect all chars till whitespace or \n or digit
        token_accumulator = []
        token_accumulator.append(c)
        while True:
            c = self.source.next_char()
            if c in [",", "(", ")", "\"", " ", "", "=", "~"]:
                self.source.prev_char()
                return "".join(token_accumulator)
            token_accumulator.append(c)
