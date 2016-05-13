#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Source:
    def __init__(self, raw_source=""):
        self._storage = []
        self._current_position = -1
        self._previous_tokens_start_position_stack = []
        for char in raw_source:
            self._storage.append(char)

    def next_char(self):
        self._current_position += 1
        if self._current_position >= len(self._storage):
            self._current_position = len(self._storage)
            return ""
        return self._storage[self._current_position]

    def prev_char(self):
        self._current_position -= 1
        if self._current_position < 0:
            self._current_position = -1
            return ""
        return self._storage[self._current_position]

    def get_current_position(self) -> int:
        return self._current_position

    def _set_current_position(self, position):
        self._current_position = position

    def push_position(self):
        # save our position for easy come back
        if not self.is_save_stack_empty():
            if self._previous_tokens_start_position_stack[-1]\
                    != len(self._storage) - 1:
                # we dont want to save last posionion every time someone call
                # next_token when there is no more chars in steam it will lead
                # to duplicated posiotions, so if last position
                # ( len (self._storage) - 1 ) is on stack then we dont save it
                # again
                self._previous_tokens_start_position_stack.append(
                    self.get_current_position())
        else:
            # is stack is empty then just push onto it
            self._previous_tokens_start_position_stack.append(
                self.get_current_position())

    def pop_position(self):
        if len(self._previous_tokens_start_position_stack) > 1:
            # remove current token start pos from stack
            self._previous_tokens_start_position_stack.pop()
            # get previous token start pos from stack
            prev_pos = self._previous_tokens_start_position_stack[-1]
            self._set_current_position(prev_pos)
        elif len(self._previous_tokens_start_position_stack) == 1:
            # we came back to begining -1 is on stack
            curr_pos = self._previous_tokens_start_position_stack.pop()
            self._set_current_position(curr_pos)

    def is_stream_end(self):
        return self._current_position == len(self._storage)

    def is_stream_start(self):
        return self._current_position == -1

    def is_save_stack_empty(self) -> bool:
        return not bool(len(self._previous_tokens_start_position_stack))

    def point_on_error(self):
        index = self.get_current_position()
        message = "".join(self._storage)
        message += "\n"
        for i in range(index):
            message += " "
        message += "^"
        return message
