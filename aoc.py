#! /usr/bin/python
"""based on advent from https://github.com/xavdid/advent-of-code-python-template"""

import argparse
import importlib

import jinja2
from loguru import logger
from pylibwfp import int_arg_range

import misc.aocConfig as config
from misc.loguruconfig import LoguruConfig
from misc.perfwatch import PerfWatch
from solutions.base import AoCException

logger.configure(handlers=[LoguruConfig()])


SOLUTION_TEMPLATE = """from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = {{ year }}
    _day = {{ day }}

    # @answer(1234)
    # def part_1(self) -> int:
    #     pass

    # @answer(1234)
    # def part_2(self) -> int:
    #     pass

    @answer((1234, 4567))
    def solve(self) -> tuple[int, int]:
        pass

"""


def newDay(args):
    logger.debug('newDay called')

    def touchFile(fspec):
        if not fspec.exists():
            fspec.touch()
        else:
            logger.info(f'not touching existing {fspec}')

    def writeSolutionFile(sdir):
        solFile = sdir / 'solution.py'
        if solFile.exists():
            logger.info(f'not touching existing {solFile}')
            return

        template = jinja2.Environment().from_string(SOLUTION_TEMPLATE)
        solFile.write_text(template.render(vars(args)))

    tlDir = config.solutionsTopLevelDir(args.year)
    tlDir.mkdir(parents=True, exist_ok=True)

    if args.day == 0:
        args.day = config.lastDay(tlDir) + 1

    solutionDir = tlDir / f'day_{args.day:02}'
    logger.info(f'Initializing {solutionDir}')

    solutionDir.mkdir(parents=True, exist_ok=True)

    touchFile(solutionDir / 'input.txt')
    touchFile(solutionDir / 'input.test.txt')

    writeSolutionFile(solutionDir)


def runDay(args):
    logger.debug('runDay() called')

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


def main():
    """main"""
    # fmt: off
    argp = argparse.ArgumentParser(description='Advent of Code templater and runner')
    argp.add_argument('--day',
                      help='day to start [1..25]',
                      type=int_arg_range(mini=0, maxi=25),
                      default=0)
    argp.add_argument('--year',
                      type=int_arg_range(mini=2015, maxi=2030),
                      default=config.DEFAULT_YEAR)

    argp_subs = argp.add_subparsers(dest='command', required=True)

    # new command with no options
    _argp_new = argp_subs.add_parser('new', help='create a template for a new day')

    # run command and options
    argp_run = argp_subs.add_parser('run', help='run a days code')
    argp_run.add_argument('-t', '--test-data',
                      action='store_true',
                      help='run using test_input.txt')
    argp_run.add_argument('--debug',
                      action='store_true',
                      help='prints normally-hidden debugging statements')
    argp_run.add_argument('--profile',
                      action='store_true',
                      help='run solution through a performance profiler')
    argp_run.add_argument('--slow',
                      action='store_true',
                      help='specify that long-running solutions (or those requiring manual input) should be run')
    argp_run.add_argument('--time',
                      action='store_true',
                      help='Print information about how long the solution (both parts) took to run')
    args = argp.parse_args()
    # fmt: on

    match args.command:
        case 'run':
            runDay(args)
        case 'new':
            newDay(args)
        case _:
            raise ValueError


if __name__ == '__main__':
    main()
