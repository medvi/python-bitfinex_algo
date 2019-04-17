"""
Entrypoint module, in case you use `python -mbitfinex_algo`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
import traceback
import logging
import sys

from bitfinex_algo.cli import main


logger = logging.getLogger('bitfinex')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%H:%M:%S')

console = logging.StreamHandler()
console.setFormatter(formatter)

logger.addHandler(console)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.error(type(e))
        logger.error(f'Unhandled error occurred:\n{traceback.format_exc()}\n')
