#!/usr/bin/env python3
"""Implement Hashcash version 1 protocol in Python
+-------------------------------------------------------+
| Written by David Mertz; released to the Public Domain |
+-------------------------------------------------------+
Very hackily modified

Double spend database not implemented in this module, but stub
for callbacks is provided in the 'check()' function

The function 'check()' will validate hashcash v1 and v0 tokens, as well as
'generalized hashcash' tokens generically.  Future protocol version are
treated as generalized tokens (should a future version be published w/o
this module being correspondingly updated).

A 'generalized hashcash' is implemented in the '_mint()' function, with the
public function 'mint()' providing a wrapper for actual hashcash protocol.
The generalized form simply finds a suffix that creates zero bits in the
hash of the string concatenating 'challenge' and 'suffix' without specifying
any particular fields or delimiters in 'challenge'.  E.g., you might get:

    >>> from hashcash import mint, _mint
    >>> mint('foo', bits=16)
    '1:16:040922:foo::+ArSrtKd:164b3'
    >>> _mint('foo', bits=16)
    '9591'
    >>> from sha import sha
    >>> sha('foo9591').hexdigest()
    '0000de4c9b27cec9b20e2094785c1c58eaf23948'
    >>> sha('1:16:040922:foo::+ArSrtKd:164b3').hexdigest()
    '0000a9fe0c6db2efcbcab15157735e77c0877f34'

Notice that '_mint()' behaves deterministically, finding the same suffix
every time it is passed the same arguments.  'mint()' incorporates a random
salt in stamps (as per the hashcash v.1 protocol).
"""
import sys
from string import ascii_letters
from math import ceil, floor
from hashlib import sha1 as sha
from random import choice
from time import strftime, localtime, time

ERR = sys.stderr            # Destination for error messages
DAYS = 60 * 60 * 24         # Seconds in a day
tries = [0]                 # Count hashes performed for benchmark

def check(stamp, resource=None, bits=None,
                 check_expiration=None, ds_callback=None):
    """Check whether a stamp is valid

    Optionally, the stamp may be checked for a specific resource, and/or
    it may require a minimum bit value, and/or it may be checked for
    expiration, and/or it may be checked for double spending.

    If 'check_expiration' is specified, it should contain the number of
    seconds old a date field may be.  Indicating days might be easier in
    many cases, e.g.

      >>> from hashcash import DAYS
      >>> check(stamp, check_expiration=28*DAYS)

    NOTE: Every valid (version 1) stamp must meet its claimed bit value
    NOTE: Check floor of 4-bit multiples (overly permissive in acceptance)
    """

    try:
        stamp_bytes = stamp.encode('ascii')
    except UnicodeError:
        ERR.write('Invalid hashcash stamp!\n')
        return False

    if stamp.startswith('0:'):          # Version 0
        try:
            date, res, suffix = stamp[2:].split(':')
        except ValueError:
            ERR.write("Malformed version 0 hashcash stamp!\n")
            return False
        if resource is not None and resource != res:
            return False
        elif check_expiration is not None:
            good_until = strftime("%y%m%d%H%M%S", localtime(time()-check_expiration))
            if date < good_until:
                return False
        elif callable(ds_callback) and ds_callback(stamp):
            return False
        elif type(bits) is not int:
            return True
        else:
            hex_digits = int(floor(bits/4))
            return sha(stamp_bytes).hexdigest().startswith('0'*hex_digits)
    elif stamp.startswith('1:'):        # Version 1
        try:
            claim, date, res, ext, rand, counter = stamp[2:].split(':')
            stamp_bytes = stamp.encode('ascii')
        except ValueError:
            ERR.write("Malformed version 1 hashcash stamp!\n")
            return False
        if resource is not None and resource != res:
            return False
        elif type(bits) is int and bits > int(claim):
            return False
        elif check_expiration is not None:
            good_until = strftime("%y%m%d%H%M%S", localtime(time()-check_expiration))
            if date < good_until:
                return False
        elif callable(ds_callback) and ds_callback(stamp):
            return False
        else:
            hex_digits = int(floor(int(claim)/4))
            return sha(stamp_bytes).hexdigest().startswith('0'*hex_digits)
    else:                               # Unknown ver or generalized hashcash
        ERR.write("Unknown hashcash version: Minimal authentication!\n")
        if type(bits) is not int:
            return True
        elif resource is not None and stamp.find(resource) < 0:
            return False
        else:
            hex_digits = int(floor(bits/4))
            return sha(stamp_bytes).hexdigest().startswith('0'*hex_digits)

def is_doublespent(stamp):
    """Placeholder for double spending callback function

    The check() function may accept a 'ds_callback' argument, e.g.
      check(stamp, "mertz@gnosis.cx", bits=20, ds_callback=is_doublespent)

    This placeholder simply reports stamps as not being double spent.
    """
    return False
