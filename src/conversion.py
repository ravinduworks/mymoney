#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Data Conversion Module"""


class DataConverter:
    """
    - Convert float string List to float values
    - Convert integer string List to integer values
    """

    @staticmethod
    def convert_to_int(data: list) -> list:
        data = map(int, data)
        data = list(data)
        return data

    @staticmethod
    def convert_to_float(data: list) -> list:
        data = map(float, data)
        data = list(data)
        return data
