#!/usr/bin/env python
# -*- coding: utf-8 -*-

from source import Source


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

    def _get_token(self):
        raise NotImplementedError("Not implemented here")

    def next_token(self) -> str:
        """
        Provide next token from stream

        Returns string or "" if EOF
        """
        self.source.push_position()
        return self._get_token()

    def prev_token(self) -> str:
        """
        Provide previous token from stream

        Returns string or "" if EOF
        """
        self.source.pop_position()
        if self.source.is_save_stack_empty():
            return ""
        return self._get_token()
