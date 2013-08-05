from idl import CorbaTypes
from ossie.utils.prop_helpers import parseComplexString
from ossie import properties

_reservedKeywords = set(("and", "as", "assert", "break", "class", "continue", "def",
                         "del", "elif", "else", "except", "exec", "finally", "for",
                         "from", "global", "if", "import", "in", "is", "lambda", "not",
                         "or", "pass", "print", "raise", "return", "try", "while",
                         "with", "yield", "None"))

def stringLiteral(value):
    return '"%s"' % (value,)

def charLiteral(value):
    return "'"+value+"'"

def stringToBoolean(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise ValueError, 'Invalid boolean literal: "%s"' % value

_typeMap = {
    CorbaTypes.BOOLEAN:   stringToBoolean,
    CorbaTypes.CHAR:      charLiteral,
    CorbaTypes.OCTET:     int,
    CorbaTypes.SHORT:     int,
    CorbaTypes.USHORT:    int,
    CorbaTypes.LONG:      int,
    CorbaTypes.ULONG:     int,
    CorbaTypes.LONGLONG:  long,
    CorbaTypes.ULONGLONG: long,
    CorbaTypes.FLOAT:     float,
    CorbaTypes.DOUBLE:    float,
    CorbaTypes.STRING:    stringLiteral,
    CorbaTypes.OBJREF:    stringLiteral,
}

def identifier(name):
    """
    Returns a valid Python identifer based on the given name.
    """
    # Replace invalid characters with '_'
    _name = ''
    for ch in name:
        if ch.isalnum():
            _name += ch
        else:
            _name += '_'
    name = _name
    # Cannot start with a digit
    if name[0].isdigit():
        name = '_' + name
    # Cannot clash with a Python keyword
    if name in _reservedKeywords:
        name += '_'
    return name

def defaultValue(typename):
    if typename in (CorbaTypes.STRING,CorbaTypes.OBJREF):
        return stringLiteral('')
    elif typename == CorbaTypes.CHAR:
        return charLiteral(' ')
    elif typename in (CorbaTypes.FLOAT,CorbaTypes.DOUBLE):
        return 0.0
    elif typename == CorbaTypes.BOOLEAN:
        return False
    else:
        return 0

def literal(value, typename, complex=False):
    if typename in _typeMap:
        if complex:
            real, imag = parseComplexString(value, typename)
            value = 'complex({0},{1})'.format(real, imag)
        else:
            value = _typeMap[typename](value)
    return value

def sequenceValue(values, typename, complex=False):
    return tuple(literal(v, typename, complex) for v in values)
