#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_filter.source import Source


class Lexer:
    """
    Base Lexer class for other lexers
    """
    def __init__(self, source: Source) -> None:
        """
        Arguments:
            - source: source - Source class object which will provide char
              stream
        """
        self.source = source

    def next_token(self) -> str:
        """
        Provide next token from stream

        Returns string or "" if EOF
        """
        self.source.push_position()
        return self._get_token()

    def next_token_no_space(self) -> str:
        """
        Provide next token from stream

        Returns string or "" if EOF
        """
        token = self.next_token()
        if token == " ":
            return self.next_token()
        else:
            return token


    def prev_token(self) -> str:
        """
        Provide previous token from stream

        Returns string or "" if EOF
        """
        self.source.pop_position()
        if self.source.is_save_stack_empty():
            return ""
        return self._get_token()

    def exception_message(self, expected, found) -> str:
        position = self.source.get_current_position()
        return "Expected {e} found {f} at {a}".format(e=repr(expected),
                f=repr(found), a=position)
