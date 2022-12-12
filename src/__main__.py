#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main argument parser module for MyMoney App"""

import os
import sys

from math import floor

from src.conversion import DataConverter
from src.sanitization import DataSanitizer
from src.manipulation import ManageDate

from src.constants import SIP
from src.constants import CHANGE
from src.constants import BALANCE
from src.constants import ALLOCATE
from src.constants import REBALANCE
from src.constants import REBALANCE_ERROR


class ManagePortfolio:
    """Investment Portfolio Tracker Module."""

    def __init__(self, file_path: str) -> None:
        try:
            if not os.path.isfile(file_path):
                print(
                    f'Invalid Input: Please input the absolute path of the file'
                )
                sys.exit(1)

        except IndexError:
            print(f'Error: File path should be absolute path!')
            sys.exit(1)

        except TypeError:
            print(
                f'Error: Exacute "python3 geektrust.py <file_path>" with the file.'
            )
            sys.exit(1)

        self.file_path = file_path
        self.monthly_data = {}

    def initialize_monthly_data(self) -> None:
        """Portfolio Setter.

        Sets the initial porfolio for equity, debt and gold. JAN is set to the
        initial allocation month while the other months are set to zero (0).
        """
        months_of_the_year = ManageDate.get_get_all_months()[1:]
        self.monthly_data = {key: [0, 0, 0] for key in months_of_the_year}
        self.monthly_data[months_of_the_year.pop(0)] = [
            self.equity_allocation,
            self.debt_allocation,
            self.gold_allocation,
        ]

    def track_portfolio(self) -> None:
        """Read investment data."""

        with open(self.file_path, 'r') as commands_file:
            for command_parameters in commands_file.readlines():
                self.run_input_command(command_parameters)

    def run_input_command(self, command_parameters: str) -> None:
        """This method takes command params, and execute the command
        appropriate command.
        """
        command = command_parameters.split(' ')[0]
        cleaned_data = DataSanitizer.clean_command(command_parameters)

        if command == ALLOCATE:
            self.allocate_funds(cleaned_data)
            self.calculate_desired_percentages()
            self.initialize_monthly_data()

        elif command == SIP:
            self.set_sip_value(cleaned_data)

        elif command == CHANGE:
            self.set_change_rates(cleaned_data)
            self.calculate_portfolio_after_change(cleaned_data[-1])

        elif command == BALANCE:
            self.get_balance(cleaned_data[0])

        elif command == REBALANCE:
            self.rebalance_investment()

        else:
            print(
                f'Invalid Input: Please provide the following options - '
                f'ALLOCATE, SIP, CHANGE, BALANCE, REBALANCE'
            )
            sys.exit(1)

    def allocate_funds(self, allocation_amounts: list) -> None:
        """This method uses a list of the initial allocation amounts and set
        the required variables.
        """
        try:
            (
                self.equity_allocation,
                self.debt_allocation,
                self.gold_allocation,
            ) = DataConverter.convert_to_int(allocation_amounts)
            self.total_allocation = (
                self.equity_allocation
                + self.debt_allocation
                + self.gold_allocation
            )

        except ValueError:
            print(
                f'Invalid Input: available options are: ALLOCATE '
                f'AMOUNT_EQUITY AMOUNT_DEBT AMOUNT_GOLD'
            )
            exit(1)

    def get_balance(self, month: str) -> None:
        equity, debt, gold = self.monthly_data.get(month)
        print(f'{equity} {debt} {gold}')

    def get_rebalanced_monthly_data(self) -> list:
        """Determines the month that should be rebalanced. Either JUN or DEC.
        If DEC data is provided, it will be the rebalance the month, if DEC is
        not available and JUN is available, JUN is returned as the rebalance month
        if none is available, it return the error.
        """
        june = ManageDate.get_get_all_months()[6]
        december = ManageDate.get_get_all_months()[12]
        december_data = self.monthly_data.get(december)
        june_data = self.monthly_data.get(june)

        if any(december_data):
            month_to_rebalance_data = december_data
            rebalance_month = december

        elif any(june_data):
            month_to_rebalance_data = june_data
            rebalance_month = june

        else:
            return REBALANCE_ERROR

        return [month_to_rebalance_data, rebalance_month]

    def rebalance_investment(self) -> None:
        """Rebalances the investment portfolio across, equity, debt and
        gold using the respective desired percentages.
        """
        try:
            (
                rebalance_month_data,
                rebalance_month,
            ) = self.get_rebalanced_monthly_data()

        except ValueError:
            print(REBALANCE_ERROR)
            return

        total_portfolio_amount = sum(rebalance_month_data)
        rebalanced_equity = floor(
            self.desired_equity_percentage * total_portfolio_amount
        )
        rebalanced_debt = floor(
            self.desired_debt_percentage * total_portfolio_amount
        )
        rebalanced_gold = floor(
            self.desired_gold_percentage * total_portfolio_amount
        )
        self.monthly_data[rebalance_month] = [
            rebalanced_equity,
            rebalanced_debt,
            rebalanced_gold,
        ]
        print(f'{rebalanced_equity} {rebalanced_debt} {rebalanced_gold}')

    def set_sip_value(self, monthly_sip_data: dict) -> bool:
        """This method sets the SIP values."""
        successful = True
        try:
            (
                self.equity_sip,
                self.debt_sip,
                self.gold_sip,
            ) = DataConverter.convert_to_int(monthly_sip_data)
            self.monthly_data[ManageDate.get_get_all_months()[0]] = [
                self.equity_sip,
                self.debt_sip,
                self.gold_sip,
            ]
        except Exception as e:
            return not successful

        return successful

    def set_change_rates(self, change_rate: list) -> bool:
        """This method sets the CHANGE rates."""
        successful = True
        try:
            (
                equity_change_rate,
                debt_change_rate,
                gold_change_rate,
            ) = DataConverter.convert_to_float(change_rate[:-1])
            self.equity_change_rate = equity_change_rate / 100
            self.debt_change_rate = debt_change_rate / 100
            self.gold_change_rate = gold_change_rate / 100
        except Exception as e:
            return not successful

        return successful

    def calculate_portfolio_after_change(self, month: str) -> None:
        """Calculates the porfolio after the change has taken effect.
        SIP is added on monthly basis starting from FEB. All data is a
        cummulation of the previous month portfolio and the respective SIP,
        except for JAN which is the Initial Month.
        """
        equity_sip = 0
        debt_sip = 0
        gold_sip = 0
        (
            previous_equity,
            previous_debt,
            previous_gold,
        ) = ManageDate.get_previous_month_data(self.monthly_data, month)
        if month != ManageDate.get_get_all_months()[1]:  # if not January
            gold_sip = self.gold_sip
            debt_sip = self.debt_sip
            equity_sip = self.equity_sip

        month_data = self.monthly_data.get(month)
        current_equity_amount = previous_equity + equity_sip
        equity_change = floor(
            current_equity_amount
            + (current_equity_amount * self.equity_change_rate)
        )

        current_debt_amount = previous_debt + debt_sip
        debt_change = floor(
            current_debt_amount + (current_debt_amount * self.debt_change_rate)
        )

        current_gold_amount = previous_gold + gold_sip
        gold_change = floor(
            current_gold_amount + (current_gold_amount * self.gold_change_rate)
        )

        month_data = [equity_change, debt_change, gold_change]
        self.monthly_data[month] = month_data

        return None

    def calculate_desired_percentages(self) -> None:
        """Set the desired percentages which is derived from the allocation ratio."""
        self.desired_equity_percentage = (
            self.equity_allocation / self.total_allocation
        )
        self.desired_debt_percentage = (
            self.debt_allocation / self.total_allocation
        )
        self.desired_gold_percentage = (
            self.gold_allocation / self.total_allocation
        )
