"""
base.py based on
https://github.com/xavdid/advent-of-code-python-template

"""

from enum import Enum, auto
from functools import wraps
from pathlib import Path
from pprint import pprint

from loguru import logger


class AoCException(Exception):
    """
    custom error class for issues related to creating/running solutions
    """


class InputTypes(Enum):
    # one solid block of text; the default
    TEXT = auto()
    # a single int
    INTEGER = auto()
    # str[], split by a specified separator (default newline)
    STRSPLIT = auto()
    # int[], split by a split by a specified separator (default newline)
    INTSPLIT = auto()


def print_answer(i, ans):
    if ans is not None:
        print(f'\n== Part {i}')
        print(f'=== {ans}')


class BaseSolution:
    separator = '\n'
    input_type = InputTypes.TEXT
    _year = None
    _day = None

    def __init__(self, *, run_slow=False, is_debugging=False, use_test_data=False):
        self.slow = run_slow
        self.is_debugging = is_debugging
        self.use_test_data = use_test_data

        self.input = self.read_input()

        if hasattr(self, '__aoc_post_init__'):
            self.__aoc_post_init__()

    @property
    def year(self):
        if self._year is None:
            raise NotImplementedError('explicitly define Solution._year')
        return self._year

    @property
    def day(self):
        if self._day is None:
            raise NotImplementedError('explicitly define Solution._day')
        return self._day

    def solve(self):
        """
        Returns a 2-tuple with the answers.
            Used instead of `part_1/2` if one set of calculations yields both answers.
        """
        return self.part_1(), self.part_2()

    def part_1(self):
        """
        Returns the answer for part 1 of the puzzle. Only needed if there's not a unified solve method.
        """
        raise NotImplementedError

    def part_2(self):
        """
        Returns the answer for part 2 of the puzzle. Only needed if there's not a unified solve method.
        """
        if self.day == 25:
            # day 25 never has a part 2
            logger.debug('skipping part 2 because day is 25')
        else:
            raise NotImplementedError

    def read_input(self):
        """
        handles locating, reading, and parsing input files
        """
        input_file = (
            Path(__file__).parent / str(self.year) / f'day_{self.day:02}' / 'input.txt'
        )

        if self.use_test_data:
            input_file = input_file.with_name(self.use_test_data)

        if not input_file.exists():
            raise AoCException(
                f'Failed to find an input file at path "./{input_file.relative_to(Path.cwd())}".'
            )

        data = input_file.read_text(encoding='utf-8').strip('\n')

        if not data:
            raise AoCException(
                f'Found a file at path "./{input_file.relative_to(Path.cwd())}", but it was empty. Make sure to paste some input!'
            )

        match self.input_type:
            case InputTypes.TEXT:
                return data
            case InputTypes.INTEGER:
                return int(data)
            case InputTypes.INTSPLIT:
                convert = int
            case InputTypes.STRSPLIT:
                convert = str
            case _:
                raise ValueError(f'Unrecognized input_type: {self.input_type}')

        return [convert(x) for x in data.split(self.separator)]

    def run_and_print_solutions(self):
        result = self.solve()
        print(f'= Solutions for {self.year} Day {self.day}')
        try:
            if result:
                p1, p2 = result
                print_answer(1, p1)
                print_answer(2, p2)
            print()
        except TypeError as exc:
            raise ValueError(
                'unable to unpack 2-tuple from `solve`, got', result
            ) from exc

    def debug(self, *objects, trailing_newline=False):
        """
        helpful debugging utility. Does nothing if `./advent` isn't passed the --debug flag

        Takes any number of objects and pretty-prints them. Can add a trailing newline to create separation between blocks
        """
        if not self.is_debugging:
            return

        for o in objects:
            pprint(o)

        if trailing_newline:
            print()


class TextSolution(BaseSolution):
    """
    input is one solid block of text; the default
    """

    input_type = InputTypes.TEXT


class IntSolution(BaseSolution):
    """
    input is a single int
    """

    input_type = InputTypes.INTEGER


class StrSplitSolution(BaseSolution):
    """
    input is a str[], split by a specified separator (default newline); specify self.separator to tweak
    """

    input_type = InputTypes.STRSPLIT


class IntSplitSolution(BaseSolution):
    """
    input is a int[], split by a specified separator (default newline); specify self.separator to tweak
    """

    input_type = InputTypes.INTSPLIT


def slow(func):
    """
    A decorator for solution methods that blocks their execution (and returns without error)
    if the the function is manually marked as "slow". Helpful if running many solutions at once,
    so one doesn't gum up the whole thing.
    """

    def wrapper(self: BaseSolution):
        if self.slow or self.use_test_data:
            return func(self)

        logger.info(f'Skipping slow function ({func.__name__})')
        return None

    return wrapper


def answer(expected):
    """
    Decorator to assert the result of the function is a certain thing.
    This is specifically designed to be used on instance methods of BaseSolution.
    It only throws errors when _not_ using test data.

    Usage:
    ```py
    @answer(3)
    def f(i):
        return i

    f(1) # throws
    f(3) # returns 3 like normal
    ```
    """

    def deco(func):
        @wraps(func)
        # uses `self` because that's what's passed to the original solution function
        def wrapper(self):
            result = func(self)
            # only assert the answer for non-test data
            if not self.use_test_data and result is not None and result != expected:
                _, year, day, _ = self.__module__.split('.')
                raise AoCException(
                    f'Failed @answer assertion for {year} / {day} / {func.__name__}:\n  returned: {result}\n  expected: {expected}'
                )
            return result

        return wrapper

    return deco
