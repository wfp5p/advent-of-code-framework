#! /usr/bin/python
"""based on advent from https://github.com/xavdid/advent-of-code-python-template"""

import argparse
import importlib

from loguru import logger
from pylibwfp import int_arg_range

import misc.aocConfig as config
from misc.perfwatch import PerfWatch
from solutions.base import AoCException


def main():
    """main"""
    # fmt: off
    argp = argparse.ArgumentParser(description='Run a specific day')
    argp.add_argument('--day',
                      help='day to start [1..25]',
                      type=int_arg_range(mini=0, maxi=25),
                      default=0)
    argp.add_argument('--year',
                      type=int_arg_range(mini=2015, maxi=2030),
                      default=config.DEFAULT_YEAR)
    argp.add_argument('-t', '--test-data',
                      action='store_true',
                      help='run using test_input.txt')
    argp.add_argument('--debug',
                      action='store_true',
                      help='prints normally-hidden debugging statements')
    argp.add_argument('--profile',
                      action='store_true',
                      help='run solution through a performance profiler')
    argp.add_argument('--slow',
                      action='store_true',
                      help='specify that long-running solutions (or those requiring manual input) should be run')
    argp.add_argument('--time',
                      action='store_true',
                      help='Print information about how long the solution (both parts) took to run')
    args = argp.parse_args()
    # fmt: on

    tlDir = config.solutionsTopLevelDir(args.year)
    if args.day == 0:
        args.day = config.lastDay(tlDir)

    # TODO: Deal with custom module paths
    solutionModuleName = (
        f'{str(tlDir / f"day_{args.day:02}").replace("/", ".")}.solution'
    )

    try:
        solutionClass = importlib.import_module(solutionModuleName).Solution
    except ModuleNotFoundError:
        logger.critical(f'error importing {solutionModuleName}')
        raise

    try:
        solution = solutionClass(
            run_slow=args.slow, is_debugging=args.debug, use_test_data=args.test_data
        )

        perfclock = PerfWatch(profile=args.profile).start()
        solution.run_and_print_solutions()
        perfclock.stop()

    except AoCException as e:
        logger.critical(e)
        raise

    if args.profile:
        perfclock.pr_stats()
        return

    if args.time:
        print(f'== Runtime\n=== Parts ran in {perfclock.runtime}s\n')


if __name__ == '__main__':
    main()
