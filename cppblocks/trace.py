# A tree-based tracing module to inspect the internals of the cppblocks library

import sys

def warning(msg):
    print >> sys.stdout, 'Warning:', msg

# A list that includes all the names of traceable modules in cppblocks
__TRACEABLE_MODULES = set([
    'cppblocks',
    'cppblocks.main',
    'cppblocks.scanner',
    'cppblocks.scanner.submodule',
    'cppblocks.parser',
    'cppblocks.parser.submodule'
])

# A set of the modules, which are currently traced.
__TRACED_MODULES = set()

# A pair of module name and option that indicates if tracing is enabled
__DO_TRACE = dict((module, False) for module in __TRACEABLE_MODULES)

def tracing_enabled(module):
    'Tests if tracing for the given module is enabled. Requires a full module path.'
    return module in __TRACEABLE_MODULES

def resolve_name(module):
    'Turns an abbreviated module name into the full module name.'
    fullName = __resolve_name(module)

    if len(fullName) > 1:
        warning("abbreviated module name '{0}' is not unique. (Possible matches: {1})".format(module, fullName))

    return fullName[0]

def __resolve_name(module):
    'Turns an abbreviated module name into the full module name. Returns all candidates.'
    fullName = filter(lambda m: m.endswith(module), __TRACEABLE_MODULES)
    return fullName

def make_shortname(fullName):
    'Turns a full module name into an abbreviated module name.'
    parts = fullName.split('.')

    shortName = parts.pop()
    while not __is_valid_shortname(shortName):
        shortName = parts.pop() + '.' + shortName

    return shortName

def __is_valid_shortname(shortName):
    fullNames = __resolve_name(shortName)
    return len(fullNames) == 1


def enable_tracing(module):
    'Enables tracing for "module" and all its sub-modules.'

    try:
        # Expand in case it is an abbreviated module name
        module = resolve_name(module)
    except:
        warning("attempt to enable tracing for unknown module '{0}'".format(module))
        return

    # subModules will also include 'module'
    subModules = filter(lambda m: m.startswith(module), __TRACEABLE_MODULES)

    __TRACED_MODULES.update(subModules)

def trace(module, *args):
    'Print a tracing message for the given module if tracing is enabled for it.'
    if not module in __TRACED_MODULES:
        return # Tracing disabled

    shortName = make_shortname(module)

    printableArgs = map(str, args)
    msg = "\n\t".join(printableArgs)

    print '{0}: {1}'.format(shortName, msg)

def enable_tracing_from_string(optionString):
    'A comma separated list of module names.'
    modules = optionString.split(',')
    for module in modules:
        enable_tracing(module)
