from redhawk.codegen.utils import parseBoolean
from ossie.utils.prop_helpers import parseComplexString
from ossie import properties

from idl import CorbaTypes

TRUE = 'true'
FALSE = 'false'

_reservedKeywords = set(("and", "and_eq", "alignas", "alignof", "asm", "auto", "bitand",
                         "bitor", "bool", "break", "case", "catch", "char", "char16_t",
                         "char32_t", "class", "compl", "const", "constexpr", "const_cast",
                         "continue", "decltype", "default", "delete", "double",
                         "dynamic_cast", "else", "enum", "explicit", "export", "extern",
                         "false", "float", "for", "friend", "goto", "if", "inline", "int",
                         "long", "mutable", "namespace", "new", "noexcept", "not",
                         "not_eq", "nullptr", "operator", "or", "or_eq", "private",
                         "protected", "public", "register", "reinterpret_cast", "return",
                         "short", "signed", "sizeof", "static", "static_assert",
                         "static_cast", "struct", "switch", "template", "this",
                         "thread_local", "throw", "true", "try", "typedef", "typeid",
                         "typename", "union", "unsigned", "using", "virtual", "void",
                         "volatile", "wchar_t", "while", "xor", "xor_eq" ))

_typeMap = {
    CorbaTypes.OCTET:     'unsigned char',
    CorbaTypes.BOOLEAN:   'bool',
    CorbaTypes.CHAR:      'char',
    CorbaTypes.SHORT:     'short',
    CorbaTypes.USHORT:    'unsigned short',
    CorbaTypes.LONG:      'CORBA::Long',
    CorbaTypes.ULONG:     'CORBA::ULong',
    CorbaTypes.LONGLONG:  'CORBA::LongLong',
    CorbaTypes.ULONGLONG: 'CORBA::ULongLong',
    CorbaTypes.FLOAT:     'float',
    CorbaTypes.DOUBLE:    'double',
    CorbaTypes.STRING:    'std::string',
    CorbaTypes.OBJREF:    'std::string'
}

_complexTypeMap = {
    CorbaTypes.FLOAT:     'std::complex<float> ',
    CorbaTypes.DOUBLE:    'std::complex<double> ',
    CorbaTypes.CHAR:      'std::complex<char> ',
    CorbaTypes.OCTET:     'std::complex<unsigned char> ',
    CorbaTypes.SHORT:     'std::complex<short> ',
    CorbaTypes.USHORT:    'std::complex<unsigned short> ',
    CorbaTypes.BOOLEAN:   'std::complex<bool> ',
    CorbaTypes.LONG:      'std::complex<CORBA::Long> ',
    CorbaTypes.ULONG:     'std::complex<CORBA::ULong> ',
    CorbaTypes.LONGLONG:  'std::complex<CORBA::LongLong> ',
    CorbaTypes.ULONGLONG: 'std::complex<CORBA::ULongLong> '
}

def stringLiteral(string):
    return '"' + string + '"'

def charLiteral(string):
    return "'" + string + "'"

def cppType(typename, complex=False):
    """
    Returns the C++ type for the given CORBA type.
    """
    if complex:
        return _complexTypeMap[typename]
    else:
        return _typeMap[typename]

def identifier(name):
    """
    Returns a valid C++ identifer based on the given name.
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
    # Cannot clash with a C++ keyword
    if name in _reservedKeywords:
        name += '_'
    return name

def literal(value, typename, complex=False):

    if complex:
        real, imag = parseComplexString(value, 
                                        typename)
        return cppType(typename, complex) + "(" + str(real) + "," + str(imag) + ")"
    elif typename == CorbaTypes.STRING:
        return stringLiteral(value)
    elif typename == CorbaTypes.BOOLEAN:
        if parseBoolean(value):
            return TRUE
        else:
            return FALSE  
    elif typename == CorbaTypes.CHAR:
        return charLiteral(value)
    else:
        return value

def sequenceType(typename, complex=False):
    return 'std::vector<%s>' % (cppType(typename, complex),)

def insert(name, typename, complex=False):
    if typename in (CorbaTypes.CHAR, CorbaTypes.OCTET) and not complex:
        return 'CORBA::Any::from_%s(%s)' % (typename, name)
    else:
        return name

def extract(name, typename, complex=False):
    if typename in (CorbaTypes.CHAR, CorbaTypes.OCTET) and not complex:
        return 'CORBA::Any::to_%s(%s)' % (typename, name)
    else:
        return name
