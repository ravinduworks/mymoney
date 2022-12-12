#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""MyMoney App Entrypoint"""

import sys

from src.__main__ import ManagePortfolio


def main():
    file_path = sys.argv[1]
    portfolio_tracker = ManagePortfolio(file_path=file_path)
    portfolio_tracker.track_portfolio()


if __name__ == '__main__':
    main()
