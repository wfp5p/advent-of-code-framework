import cProfile
import time


class PerfWatch:
    startTime: int = 0
    stopTime: int = 0
    _pr: None

    def __init__(self, *, profile=False):
        if profile:
            self._pr = cProfile.Profile()
        else:
            self._pr = None

    def start(self):
        self.startTime = time.monotonic_ns()
        if self._pr:
            self._pr.enable()
        return self

    def stop(self):
        self.stopTime = time.monotonic_ns()
        if self._pr:
            self._pr.disable()

    def pr_stats(self, *, sort_order='tottime'):
        if not self._pr:
            return
        self._pr.print_stats(sort=sort_order)

    @property
    def runtime_ns(self) -> int:
        if self.stopTime < self.startTime:
            return 0

        return self.stopTime - self.startTime

    @property
    def runtime(self):
        return round(self.runtime_ns / 1_000_000_000, 3)
