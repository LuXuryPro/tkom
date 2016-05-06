#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lexer import Lexer


class HTTPLexerException(Exception):
    pass


class HTTPLexer(Lexer):
    def _get_token(self) -> str:
        """
        private _get_token

        _get_token method sepcific for HTTPLexer
        """
        c = self.source.next_char()
        # go throught all spaces and return only one
        if c == " ":
            while c == " ":
                c = self.source.next_char()

            self.source.prev_char()
            return " "
        # one char tokens can be returned immediately
        if c in ["/", ".", ":"]:
            return c
        # if next char is \n that means \r is missing beafore it and that is an
        # error
        if c == "\n":
            raise HTTPLexerException("Not expected \\n at {pos}".format(
                pos=self.source.get_current_position()))
        if c == "\r":
            # here we expect that next char is \n (LF)
            lf = self.source.next_char()
            if lf == "\n":
                return "\r\n"
            else:
                # we have error \r is not beafore \n
                raise HTTPLexerException(
                        "Expected \\n at {pos} found {c}".format(
                            pos=self.source.get_current_position(), c=lf))

        # digits
        if c.isdigit():
            return c

        # collect all chars till whitespace or \n or digit
        token_accumulator = []
        token_accumulator.append(c)
        while True:
            c = self.source.next_char()
            if c == "":
                return c
            if c in ["/", ".", ":", "\n", "\r", " "]:
                self.source.prev_char()
                return "".join(token_accumulator)
            token_accumulator.append(c)
