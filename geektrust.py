#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""MyMoney App Entrypoint"""

from src.__main__ import PortfolioTracker


def main():
    portfolio_tracker = PortfolioTracker()
    portfolio_tracker.track_portfolio()


if __name__ == '__main__':
    main()
