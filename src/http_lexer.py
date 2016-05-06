#!/usr/bin/env python
# -*- coding: utf-8 -*-

class HTTPLexerException(Exception):
    pass

class HTTPLexer:
    def __init__(self, source):
        self.source = source
        self.token_start_position = 0
        self.prev_tokens_start_pos = []

    def get_token(self):
        self.source.push_pos()
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
        # if next char is \n that means \r is missing beafore it and that is an error
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
                raise HTTPLexerException("Expected \\n at {pos} found {c}".format(
                    pos=self.source.get_current_position(), c=lf))

        # digits
        if c.isdigit():
            return c

        # collect all chars till whitespace or \n or digit
        token_accumulator = []
        token_accumulator.append(c)
        while True:
            self.source.push_pos()
            c = self.source.next_char()
            if c == "":
                return c
            if c in ["/", ".", ":", "\n", "\r", " "]:
                self.source.pop_pos()
                return "".join(token_accumulator)
            token_accumulator.append(c)

    def next_token(self):
        # save our positon for easy come back
        self.prev_tokens_start_pos.append(self.source.get_current_position())
        return self.get_token()

    def prev_token(self):
        if len(self.prev_tokens_start_pos) > 1:
            # remove current token start pos from stack
            curr_pos = self.prev_tokens_start_pos.pop()
            # get previous token start pos from stack
            prev_pos = self.prev_tokens_start_pos[-1]
            self.source.set_current_position(prev_pos)
            return self.get_token()
        else:
            # we came back to begining
            self.source.set_current_position(-1)
            return ""

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
