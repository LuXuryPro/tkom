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
        # go throught all spaces
        while c == " ":
            c = self.source.next_char()
        # one char tokens
        if c in ["/", ".", ":"]:
            return c
        if c == "\n":
            raise HTTPLexerException("Expected \\r at {pos} found \\n".format(
                pos=self.source.get_current_position()))
        if c == "\r":
            # here w expect that next char is \n (LF)
            lf = self.source.next_char()
            if lf == "\n":
                return "\r\n"
            else:
                # we have error
                raise HTTPLexerException("Expected \\n at {pos} found {c}".format(
                    pos=self.source.get_current_position(), c=lf))

        self.source.push_pos()
        if c == "H":
            if self.source.next_char() == "T":
                if self.source.next_char() == "T":
                    if self.source.next_char() == "P":
                        return "HTTP"
        self.source.pop_pos()

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
        self.prev_tokens_start_pos.append(self.source.get_current_position())
        return self.get_token()

    def prev_token(self):
        if len(self.prev_tokens_start_pos) != 0:
            curr_pos = self.prev_tokens_start_pos.pop()
            prev_pos = self.prev_tokens_start_pos.pop()
            self.source.set_current_position(prev_pos)
            return self.get_token()
        else:
            self.source.set_current_position(-1)
            return ""


