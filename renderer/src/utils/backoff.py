"""Backoff decorators."""

import logging
from functools import wraps
from time import sleep
from typing import Any, Tuple

logger = logging.getLogger(__name__)


def compute_delay(
    start_sleep_time: float,
    factor: float,
    border_sleep_time: float,
    delay: float,
    retry: int,
) -> Tuple[int, float]:
    """Compute delay for the next itteration.
     Args:
        start_sleep_time: Initial time to repeat.
        factor: Multiplier of time.
        border_sleep_time: Max time.
        delay: Last delay.
        retry: Number of the itteration.
    Returns:
        Tuple[int, float]: Tuple calculated retry and delay.
    """
    if delay < border_sleep_time:
        delay = start_sleep_time * (factor ** retry)
    return retry + 1, delay


def backoff_reconnect(
        start_sleep_time: float = 0.1,
        factor: float = 2,
        border_sleep_time: float = 10
) -> Any:
    """Retry with reconnect and delay.
    The function tries to call an argument function after reconnect and delay if the argument
    function caused an exception.
    Args:
        start_sleep_time: Initial time to repeat.
        factor: Multiplier of time.
        border_sleep_time: Max time.
    Returns:
        Any: Result of calling function.
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            retry = 1
            delay = start_sleep_time
            while True:
                try:
                    return func(self, *args, **kwargs)
                except Exception:
                    sleep_time = min(delay, border_sleep_time)
                    logger.exception(
                        'Error in {func}. Next try in {sec} seconds'.format(
                            sec=sleep_time,
                            func=str(func),
                        ),
                    )
                    sleep(sleep_time)
                    retry, delay = compute_delay(
                        start_sleep_time=start_sleep_time,
                        factor=factor,
                        border_sleep_time=border_sleep_time,
                        delay=delay,
                        retry=retry,
                    )
                    self.reconnect()
        return inner
    return func_wrapper


def backoff(
        start_sleep_time: float = 0.1,
        factor: float = 2,
        border_sleep_time: float = 10
) -> Any:
    """Retry call a function with delay.
    The function tries to call an argument function after delay if the argument
    function caused an exception.
    Args:
        start_sleep_time: Initial time to repeat.
        factor: Multiplier of time.
        border_sleep_time: Max time.
    Returns:
        Any: Result of calling function.
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            retry = 1
            delay = start_sleep_time
            while True:
                try:
                    return func(self, *args, **kwargs)
                except Exception:
                    logger.exception(
                        'Error in {func}. Next try in {sec} seconds'.format(
                            sec=min(delay, border_sleep_time),
                            func=str(func),
                        ),
                    )
                    sleep(min(delay, border_sleep_time))
                    retry, delay = compute_delay(
                        start_sleep_time=start_sleep_time,
                        factor=factor,
                        border_sleep_time=border_sleep_time,
                        delay=delay,
                        retry=retry,
                    )
        return inner
    return func_wrapper
