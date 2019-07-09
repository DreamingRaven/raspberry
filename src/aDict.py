# @Author: archer
# @Date:   2019-07-09T13:21:57+01:00
# @Last modified by:   archer
# @Last modified time: 2019-07-09T13:22:06+01:00
# @License: Please see LICENSE in project root



from __future__ import print_function           # python 2-3 compat print
try:                                            # python 3
    from collections.abc import MutableMapping
except ImportError:                             # python 2
    from collections import MutableMapping

import os
import sys


class ADict(MutableMapping):
    """
    Abstract dictionary class for standardisation of database input, python2/3.
    """

    def __init__(self, dictz=None):
        self.dict = dictz if dictz is not None else dict()

    def __getitem__(self, key):
        try:
            return self.dict[key]
        except KeyError:
            pass  # what was asked does not exist which is the same as None so will not error
        except TypeError:
            print("TypeError: cannot use:", key,
                  "with object:", type(self.dict))

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __delitem__(self, key):
        try:
            del self.dict[key]
        except KeyError:
            pass  # job is not done but equivelant outcomes so will not error

    def __iter__(self):
        return iter(self.dict)

    def __len__(self):
        return len(self.dict)

    def swapDict(self, newDict):
        oldDict = self.dict
        self.dict = newDict
        return oldDict


# tests on overloaded functions to check functionality is correct!
if(__name__ == "__main__"):

    dictz = {
        "notFlower": "teaspoon",
        "chief": 117,
        "dingDong": "theWitchIsDead",
    }
    dictz2 = {
        "flower": "buttercup",
        "jimmy": 69,
        "my name is phil": "nice to meet you phil",
    }

    # check init
    duct = ADict(dictz=dictz)
    # check changing dict is possible
    oldDict = duct.swapDict(dictz2)
    # check getting value is possible
    value = duct["flower"]
    # check setting value is possible
    duct["flower"] = 64
    # check dleting key is possible (but depend on dict swap working)
    del duct["flower"]
    # check dict is iteratable
    for key in duct:
        str(key + " : " + str(duct[key]) + " " + str(len(duct)))
    # check dict does not throw error if key is missued and returns None
    didError = duct["jimmyridler"]
