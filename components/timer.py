import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(name)s: %(message)s',
    level=logging.INFO
)


def time_of_function(function):
    """Вычисление времени выполнения функции"""

    def wrapped(*args):
        start_time = time.perf_counter_ns()
        res = function(*args)
        time_execute = round((time.perf_counter_ns() - start_time) / pow(10, 6), 2)
        logger.info('Время выполнения расчета функции {}: {} милисекунд'.format(function.__name__, time_execute))
        return res
    return wrapped