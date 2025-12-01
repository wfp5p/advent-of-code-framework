from pathlib import Path

DEFAULT_YEAR = 2025


def solutionsTopLevelDir(year: int) -> Path:
    return Path('solutions') / str(year)


def lastDay(tlDir: Path) -> int:
    """return the number of the last day directory"""
    return max(
        [0]
        + [
            int(x.name.removeprefix('day_'))
            for x in tlDir.glob('day_[0-9][0-9]')
            if x.is_dir()
        ]
    )
