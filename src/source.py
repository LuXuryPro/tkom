#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Source:
    def __init__(self, raw_source=""):
        self.__storage = []
        self.__current = -1
        self.__saved_pos = -1
        self.__line = 0
        for char in raw_source:
            self.__storage.append(char)

    def next_char(self):
        self.__current += 1
        if self.__current >= len(self.__storage):
            self.__current = len(self.__storage)
            return ""
        return self.__storage[self.__current]

    def prev_char(self):
        self.__current -= 1
        if self.__current < 0:
            self.__current = -1
            return ""
        return self.__storage[self.__current]

    def get_current_position(self):
        return self.__current

    def set_current_position(self, position):
        self.__current = position

    def push_pos(self):
        self.__saved_pos = self.__current

    def pop_pos(self):
        self.__current = self.__saved_pos



