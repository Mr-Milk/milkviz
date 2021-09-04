import re
from inspect import getdoc

PARAMETERS_DOCSTRINGS = dict(

)


def doc(obj):
    docstring = getdoc(obj)
    for param_name, content in PARAMETERS_DOCSTRINGS.items():
        pattern = re.compile(f"(:param: {param_name})")
        docstring = re.sub(pattern, content, docstring)
    obj.__doc__ = docstring
    return obj
