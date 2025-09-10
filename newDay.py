#! /usr/bin/python
"""based on start from https://github.com/xavdid/advent-of-code-python-template"""

import argparse

import jinja2
from loguru import logger
from pylibwfp import int_arg_range

import misc.aocConfig as config

SOLUTION_TEMPLATE = """

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = {{ year }}
    _day = {{ day }}

    # @answer(1234)
    def part_1(self) -> int:
        pass

    # @answer(1234)
    def part_2(self) -> int:
        pass

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass

"""


def touchFile(fspec):
    if not fspec.exists():
        fspec.touch()
    else:
        logger.info(f'not touching existing {fspec}')


def writeSolutionFile(sdir, args):
    solFile = sdir / 'solution.py'
    if solFile.exists():
        logger.info(f'not touching existing {solFile}')
        return

    template = jinja2.Environment().from_string(SOLUTION_TEMPLATE)
    solFile.write_text(template.render(args))


def main():
    """main"""
    # fmt: off
    argp = argparse.ArgumentParser(description='Template a new day')
    argp.add_argument('--day',
                      help='day to start [1..25]',
                      type=int_arg_range(mini=0, maxi=25),
                      default=0)
    argp.add_argument('--year',
                      type=int_arg_range(mini=2015, maxi=2030),
                      default=config.DEFAULT_YEAR)
    args = argp.parse_args()
    # fmt: on

    tlDir = config.solutionsTopLevelDir(args.year)
    tlDir.mkdir(parents=True, exist_ok=True)

    if args.day == 0:
        args.day = config.lastDay(tlDir) + 1

    solutionDir = tlDir / f'day_{args.day:02}'
    logger.info(f'Initializing {solutionDir}')

    solutionDir.mkdir(parents=True, exist_ok=True)

    touchFile(solutionDir / 'input.txt')
    touchFile(solutionDir / 'input.test.txt')

    writeSolutionFile(solutionDir, vars(args))


if __name__ == '__main__':
    main()
