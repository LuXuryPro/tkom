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
            - source: source - Source class object which will provide char stream
        """
        self.source = source
        self.prev_tokens_start_pos = []

    def _get_token(self):
        raise NotImplementedError( "Not implemented here" )

    def next_token(self) -> str:
        """
        Provide next token from stream

        Returns string or "" if EOF
        """
        # save our positon for easy come back
        if not self.source.is_stream_end(): 
            # we dont want to save same posionion every time someone call next_token when
            # there is no more chars in steam it will lead to duplicated posiotions
            self.prev_tokens_start_pos.append(self.source.get_current_position())
            return self._get_token()
        else:
            return ""

    def prev_token(self) -> str:
        """
        Provide previous token from stream

        Returns string or "" if EOF
        """
        if len(self.prev_tokens_start_pos) > 1:
            # remove current token start pos from stack
            curr_pos = self.prev_tokens_start_pos.pop()
            # get previous token start pos from stack
            prev_pos = self.prev_tokens_start_pos[-1]
            self.source.set_current_position(prev_pos)
            return self._get_token()
        elif len(self.prev_tokens_start_pos) == 1:
            # we came back to begining -1 is on stack
            curr_pos = self.prev_tokens_start_pos.pop()
            self.source.set_current_position(curr_pos)
        return ""

