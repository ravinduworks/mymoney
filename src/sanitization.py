#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Data Sanitization Module"""


class DataSanitizer:
    """Function does Following:
    - Removes new line character from the string
    - Removes the any special characters such as percentage sign and extra space
    """

    @staticmethod
    def clean_command(command_parameters: str) -> list:
        cleaned_command: list = command_parameters.strip('\n')
        cleaned_command: list = cleaned_command.replace('%', '')
        cleaned_command: list = cleaned_command.split(' ')[1:]

        return cleaned_command
