"""
This is a little test script to talk about
Python modules and scope.

We may get to it in lecture 1 or in a future lecture.
"""

print("Python modules and scope")

import sys
import types
def imports():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__

print("__name__:", __name__)
print("All modules:", sys.modules.keys())
print("Local modules:", list(imports()))
print("This module:", sys.modules[__name__])
print("This module:", sys.modules[__name__].__name__)
