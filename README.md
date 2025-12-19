# Python Framework for Advent of Code

A framework to handle the busy work for [Advent of Code](https://adventofcode.com/) puzzles. 

Based on the [@xavid's template](https://github.com/xavdid/advent-of-code-python-template) 

## Usage

`aoc.py` is the only executable script.  It has options to set up a skeleton for a new day's solution or run a
particular day's solution.

The `--year YEAR` and `--day DAY` options are available to set the year and day of the solution you would like
to create or run.  If omitted they will default to today's date.

### Starting a new puzzle

> `./aoc.py [--year YEAR] [--day DAY] new [--baseclass {TextSolution,IntSolution,StrSplitSolution,IntSplitSolution}'

Creates a new solution framework in the directory solutions/YEAR/day_DAY

The `solution.py` file is created using file in `misc/solution.py.j2`.

### Running a specific puzzle

> `./aoc.py [--year YEAR] [--day DAY] run [-t [TEST_DATA]] [--solution SOLUTION_MODULE] [--debug] [--profile] [--slow] [--time]`

**optional flags**

- `-t, --test-data [TEST_DATA]`: read puzzle input from file TEST_DATA. If no filename is given, defaults to `input.test.txt`
- `--solution, --solution_module SOLUTION_MODULE`: use a solution module different from the default `solution.py`
- `--debug`: prints debug statments and sets the default logger level to DEBUG
- `--profile`: run solution through a performance profiler
- `--slow`: skip running solutions flagged with the `@slow` decorator
- `--time`: print duration of run information

#### Examples

- `./aoc.py run`
- `./aoc.py run -t`
- `./aoc.py run -t input.test.txt.2`
- `./aoc.py --year 2025 --day 10 run`
- `./aoc.py --year 2025 --day 10 run --solution solution2.py`
