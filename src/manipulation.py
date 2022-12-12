#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Data Manipulation module"""

import calendar


class ManageDate:
    """Data Manupulater Module"""

    @classmethod
    def get_previous_month(cls, current_month) -> list:
        """Return the previous month string from the current month."""

        all_months = cls.get_get_all_months()[1:]
        current_month_index = all_months.index(current_month)
        if current_month_index == 0:
            return current_month

        previous_month = all_months[current_month_index - 1]
        return previous_month

    @classmethod
    def get_previous_month_data(
        cls, monthly_data: dict, current_month: str
    ) -> list:
        """Returns a list of the portfolio(equity, debt, gold) of the previous
        month from the current month.
        """
        previous_month = cls.get_previous_month(current_month)
        previous_month_data = monthly_data.get(previous_month)
        return previous_month_data

    @staticmethod
    def get_get_all_months() -> list:
        """Returns a list of all the months(JAN-DEC)"""
        months = list(map(str.upper, calendar.month_name))
        return months
