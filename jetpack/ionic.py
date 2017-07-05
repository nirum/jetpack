# -*- coding: utf-8 -*-
"""
Ionic
-----

IO and display utilities
"""
import sys
import warnings
from contextlib import contextmanager
from numbers import Number

import numpy as np

try:
    from pushover import Client
except ImportError:
    warning = """Pushover not installed, push() function disabled.
                 Use 'pip install python-pushover' to install pushover."""
    warnings.warn(warning)

    class Client(object):
        def __init__(self):
            pass

        def send_message(self, *args, **kwargs):
            warnings.warn(warning)

try:
    from emoji import emojize
except ImportError:
    warning = """Emoji not installed, strings will not emojize automatically.
                 Use 'pip install emoji' to get this feature."""
    warnings.warn(warning)

    def emojize(x, *args, **kwargs):
        return x

__all__ = ['csv', 'as_percent', 'notify', 'unicodes', 'push', 'pem']


def csv(filename, data, headers=None, fmt='%g'):
    """
    Write a numpy array to a CSV file with the given headers

    Parameters
    ----------
    filename : string
        The filename of the CSV file to write

    data : array_like
        A numpy array (matrix) containing the data to write

    headers : list, optional
        List of strings corresponding to the column headers (default: None)

    fmt : string, optional
        A format string for how to encode the data (default: '%g')
    """
    assert data.ndim == 2, "Data must be a matrix (have two dimensions)"

    if not filename.endswith('.csv'):
        filename += '.csv'

    if headers:

        assert data.shape[1] == len(headers), \
            "Data must have the same number of columns as the headers"

        hdr = ','.join(headers)

    else:
        hdr = ''

    np.savetxt(filename, data, delimiter=',', fmt=fmt, header=hdr, comments='')


def as_percent(x, precision='0.2'):
    """
    Convert number to percentage string.
    """
    if isinstance(x, Number):
        return "{{:{}%}}".format(precision).format(x)
    else:
        raise TypeError("Numeric type required")


def push(message, title=''):
    """
    Send a notification via pushover

    Parameters
    ----------
    message : string

    title : string, optional

    """
    Client().send_message(emojize(message, use_aliases=True),
                          title=emojize(title, use_aliases=True))


def pem(message):
    """
    Print an emoijized string

    Parameters
    ----------
    message : string

    """
    print(emojize(message, use_aliases=True))


@contextmanager
def notify(title='Loading'):
    """
    Context manager for printing messages of the form 'Loading... Done.'

    Parameters
    ----------
    title : string
        A message / title to print (Default: 'Loading')

    Usage
    -----
    with notify('Working'):
        # do long running task
        time.sleep(0.5)
    >>> -> Working... Done.

    """

    print(f"{unicodes['arrow']}  {title}...", end='')
    sys.stdout.flush()
    try:
        yield
    finally:
        print(f"Done! {unicodes['check']}")


unicodes = {
    'mu': u'\u03BC',
    'degrees': u'\u00B0',
    'micro': u'\u00B5',
    'lambda': u'\u03BB',
    'gamma': u'\u03B3',
    'pi': u'\u03C0',
    'Pi': u'\u220F',
    'tau': u'\u03C4',
    'sigma': u'\u03C3',
    'rho': u'\u03C1',
    'kappa': u'\u03BA',
    'theta': u'\u03B8',
    'epsilon': u'\u03B5',
    'delta': u'\u03B4',
    'Delta': u'\u0394',
    'phi': u'\u03C6',
    'Phi': u'\u03A6',
    'check': u'\u2714',
    'x': u'\u2718',
    'star': u'\u272F',
    'arrow': u'\u279B',
    'pm': u'\u00B1',
    'gradient': u'\u2206',
    'nabla': u'\u2207',
    'in': u'\u2208',
    'exists': u'\u2203',
    'forall': u'\u2200',
    'not_in': u'\u2209',
    'int': u'\u222B',
    'grad': u'\u2202',
    'partial': u'\u2202',
    'sqrt': u'\u221A',
    'geq': u'\u2265',
    'leq': u'\u2264',
    'neq': u'\u2260',
    'approx': u'\u2243',
    'infty': u'\u221E',
    'cdot': u'\u2219',
    'Sigma': u'\u2211',
    'sum': u'\u2211',
    'prod': u'\u220F',
    'cloud': u'\u2601',
    'umbrella': u'\u2602',
    'snowflake': u'\u2600',
    'dollar': u'\u0024',
}
