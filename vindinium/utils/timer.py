"""Timer utility for measuring code execution time.

This module provides a Timer class that can be used as a context manager
or with tic/toc methods similar to MATLAB.
"""

import time

__all__ = ['Timer']


class Timer:
    """Timer helper for measuring code execution time.

    A timer object helps to measure how much time has been taken to execute
    some code.

    Example:
        You can use this class in two ways. First as a context manager::

            with Timer() as timer:
                # your code here
            print(timer.elapsed)

        You can pass ``True`` as argument to Timer to automatically
        print the elapsed time when the context exits.

        Alternatively, you can use Timer like the tic/toc functions of MATLAB::

            timer = Timer()
            timer.tic()
            # your code here
            print(timer.toc())

    Attributes:
        elapsed (float): The elapsed time between ``tic()`` and ``toc()``.
    """

    def __init__(self, do_print=False):
        """Initialize the timer.

        Args:
            do_print (bool): Whether timer should print the result after
                the context manager exits. Defaults to False.
        """
        self._do_print = do_print
        self._start_time = 0
        self.elapsed = 0

    def __enter__(self):
        """Enter the context manager and start the timer.

        Returns:
            Timer: This timer instance.
        """
        self.tic()
        return self

    def __exit__(self, type, value, traceback):
        """Exit the context manager and stop the timer.

        Args:
            type: Exception type (if any).
            value: Exception value (if any).
            traceback: Exception traceback (if any).
        """
        self.toc()

        if self._do_print:
            print('Elapsed time is %f seconds.' % self.elapsed)

    def tic(self):
        """Start the timer."""
        self._start_time = time.time()

    def toc(self):
        """Stop the timer and return the elapsed time.

        Returns:
            float: The elapsed time in seconds.
        """
        self.elapsed = time.time() - self._start_time
        return self.elapsed
