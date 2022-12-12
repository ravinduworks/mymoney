#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main argument parser module for MyMoney App"""

import os
import sys

from math import floor

from src.conversion import DataConverter
from src.sanitization import DataSanitizer
from src.manipulation import DateManupulationServices

from src.constants import SIP
from src.constants import CHANGE
from src.constants import BALANCE
from src.constants import ALLOCATE
from src.constants import REBALANCE
from src.constants import REBALANCE_ERROR


class PortfolioTracker:
    def __init__(self) -> None:
        try:
            file_path = sys.argv[1]
            if not os.path.isfile(file_path):
                print(
                    f'Invalid File: to run file execute "python3 geektrust.py <file_path>"'
                )
                sys.exit(1)

        except IndexError:
            print(f'Error: Supply a file path')
            sys.exit(1)

        except TypeError:
            print(f'Error: to run the file execute "python3 geektrust.py <file_path>"')
            sys.exit(1)

        self.file_path = file_path
        self.monthly_data = {}

    def initialize_monthly_data(self) -> None:
        """Portfolio Setter.

        Sets the initial porfolio for equity, debt and gold
        January is set to the initial allocation while the
        other months are set to 0.
        """
        months_of_the_year = DateManupulationServices.get_get_all_months()[1:]
        self.monthly_data = {key: [0, 0, 0] for key in months_of_the_year}
        self.monthly_data[months_of_the_year.pop(0)] = [
            self.equity_allocation,
            self.debt_allocation,
            self.gold_allocation,
        ]

    def track_portfolio(self) -> None:
        """Read investment data.

        This is the main method opens the input file,
        reads it line by line and calls the method that
        execute the command on the line.
        """
        with open(self.file_path, 'r') as commands_file:
            for command_parameters in commands_file.readlines():
                self.execute_next_command(command_parameters)

    def execute_next_command(self, command_parameters: str) -> None:
        """This method takes command parameters, and execute the command 
        appropriate command.
        """
        command = command_parameters.split(' ')[0]
        cleaned_data = DataSanitizer.clean_command(command_parameters)

        if command == ALLOCATE:
            self.allocate_funds(cleaned_data)
            self.calculate_desired_percentages()
            self.initialize_monthly_data()

        elif command == SIP:
            self.set_sip_values(cleaned_data)

        elif command == CHANGE:
            self.set_change_rates(cleaned_data)
            self.calculate_portfolio_after_change(cleaned_data[-1])

        elif command == BALANCE:
            self.get_balance(cleaned_data[0])

        elif command == REBALANCE:
            self.rebalance_investment()

        else:
            print(
                f'Please enter a valid command. choices are: ALLOCATE, SIP, '
                f'CHANGE, BALANCE, REBALANCE'
            )
            sys.exit(1)

    def allocate_funds(self, allocation_amounts: list) -> None:
        """This method takes a list of the initial allocation amounts and set 
        the respective variables.
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
                f'Please supply a valid command format is: ALLOCATE '
                f'AMOUNT_EQUITY AMOUNT_DEBT AMOUNT_GOLD'
            )
            exit(1)

    def get_balance(self, month: str) -> None:
        equity, debt, gold = self.monthly_data.get(month)
        print(f'{equity} {debt} {gold}')

    def get_rebalance_month_data(self) -> list:
        """
        This method determines the month that should be rebalanced.
        It is either June or December. If December data is available,
        it will be the rebalance month, if December is not available
        and June is available, June is returned as the rebalance month
        if none is available, then rebalance error is returned.
        """
        june = DateManupulationServices.get_get_all_months()[6]
        december = DateManupulationServices.get_get_all_months()[12]
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
        """This rebalances the investment portfolio across, equity, debt and 
        gold using the respective desired percentages.
        """
        try:
            (
                rebalance_month_data,
                rebalance_month,
            ) = self.get_rebalance_month_data()

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

    def set_sip_values(self, monthly_sip_data: dict) -> bool:
        """This method sets the SIP values.
        """
        successful = True
        try:
            (
                self.equity_sip,
                self.debt_sip,
                self.gold_sip,
            ) = DataConverter.convert_to_int(monthly_sip_data)
            self.monthly_data[
                DateManupulationServices.get_get_all_months()[0]
            ] = [
                self.equity_sip,
                self.debt_sip,
                self.gold_sip,
            ]
        except Exception as e:
            return not successful

        return successful

    def set_change_rates(self, change_rate: list) -> bool:
        """This method sets the CHANGE rates.
        """
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
        """This method calculates the porfolio after the change has taken effect. 
        SIP is added on monthly basis starting from February. All data is a 
        cummulation of the previous month portfolio and the respective sip, 
        except for January which is the initial month.
        """
        equity_sip = 0
        debt_sip = 0
        gold_sip = 0
        (
            previous_equity,
            previous_debt,
            previous_gold,
        ) = DateManupulationServices.get_previous_month_data(
            self.monthly_data, month
        )
        if (
            month != DateManupulationServices.get_get_all_months()[1]
        ):  # if not January
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
        """Function to set the desired percentages which is derived from the 
        allocation ratio.
        """
        self.desired_equity_percentage = (
            self.equity_allocation / self.total_allocation
        )
        self.desired_debt_percentage = (
            self.debt_allocation / self.total_allocation
        )
        self.desired_gold_percentage = (
            self.gold_allocation / self.total_allocation
        )
