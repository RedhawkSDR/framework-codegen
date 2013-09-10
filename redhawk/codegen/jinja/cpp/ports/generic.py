import jinja2
from omniORB import CORBA

from redhawk.codegen.lang import cpp
from redhawk.codegen.jinja.ports import PortFactory
from redhawk.codegen.jinja.cpp import CppTemplate

from generator import CppPortGenerator

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

_baseMap = {
    CORBA.tk_short:     'CORBA::Short',
    CORBA.tk_long:      'CORBA::Long',
    CORBA.tk_ushort:    'CORBA::UShort',
    CORBA.tk_ulong:     'CORBA::ULong',
    CORBA.tk_float:     'CORBA::Float',
    CORBA.tk_double:    'CORBA::Double',
    CORBA.tk_boolean:   'CORBA::Boolean',
    CORBA.tk_char:      'CORBA::Char',
    CORBA.tk_octet:     'CORBA::Octet',
    CORBA.tk_longlong:  'CORBA::LongLong',
    CORBA.tk_ulonglong: 'CORBA::ULongLong'
}

def baseType(typeobj):
    kind = typeobj.kind()
    if kind in _baseMap:
        return _baseMap[kind]
    elif kind == CORBA.tk_void:
        return 'void'
    elif kind == CORBA.tk_string:
        return 'char*'
    elif kind == CORBA.tk_any:
        return 'CORBA::Any'
    
    name = '::'.join(typeobj.scopedName())
    if kind == CORBA.tk_objref:
        return name + '_ptr'
    else:
        return name

def baseReturnType(typeobj):
    kind = typeobj.kind()
    if kind in _baseMap:
        return _baseMap[kind]
    elif kind == CORBA.tk_void:
        return 'void'
    elif kind == CORBA.tk_string:
        return 'char*'
    elif kind == CORBA.tk_any:
        return 'CORBA::Any'
    
    name = '::'.join(typeobj.scopedName())
    if kind == CORBA.tk_objref:
        return name + '_ptr'
    elif kind == CORBA.tk_alias or kind == CORBA.tk_struct:
        return name + '*'
    else:
        return name

def paramType(param):
    name = baseType(param.paramType)
    if not param.direction == 'in':
        return name + '&'
    kind = param.paramType.kind()
    if kind in _baseMap:
        return name
    else:
        name = 'const '+name
    if kind == CORBA.tk_string or kind == CORBA.tk_objref:
        return name
    return name + '&'

class GenericPortFactory(PortFactory):
    def match(self, port):
        return True

    def generator(self, port):
        if port.isProvides():
            return GenericProvidesPortGenerator(port)
        else:
            return GenericUsesPortGenerator(port)

class GenericPortGenerator(CppPortGenerator):
    def _ctorArgs(self, name):
        return (cpp.stringLiteral(name), 'this')

    def loader(self):
        return jinja2.PackageLoader(__package__)

    def operations(self):
        for op in self.idl.operations():
            yield {'name': op.name,
                   'arglist': ', '.join('%s %s' % (paramType(p), p.name) for p in op.params),
                   'argnames': ', '.join(p.name for p in op.params),
                   'returns': baseReturnType(op.returnType)}
        for attr in self.idl.attributes():
            yield {'name': attr.name,
                   'arglist': '',
                   'argnames': '',
                   'returns': baseReturnType(attr.attrType)}
            if not attr.readonly:
                yield {'name': attr.name,
                       'arglist': baseType(attr.attrType) + ' data',
                       'argnames': 'data',
                       'returns': 'void'}

class GenericUsesPortGenerator(GenericPortGenerator):
    def headers(self):
        return ('<ossie/CF/QueryablePort.h>',)

    def _declaration(self):
        return CppTemplate('generic.uses.h')

    def _implementation(self):
        return CppTemplate('generic.uses.cpp')

class GenericProvidesPortGenerator(GenericPortGenerator):
    def _declaration(self):
        return CppTemplate('generic.provides.h')

    def _implementation(self):
        return CppTemplate('generic.provides.cpp')
