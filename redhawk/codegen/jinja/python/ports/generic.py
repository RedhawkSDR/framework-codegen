import jinja2
from omniORB import CORBA

from redhawk.codegen.lang import python
from redhawk.codegen.jinja.ports import PortFactory
from redhawk.codegen.jinja.python import PythonTemplate

from generator import PythonPortGenerator

class GenericPortFactory(PortFactory):
    def match(cls, port):
        return True

    def generator(cls, port):
        if port.isProvides():
            return GenericPortGenerator('generic.provides.py', port)
        else:
            return GenericPortGenerator('generic.uses.py', port)

class GenericPortGenerator(PythonPortGenerator):
    def __init__(self, template, port):
        super(GenericPortGenerator,self).__init__(port)
        self.__template = PythonTemplate(template)

    def _ctorArgs(self, port):
        return ('self', python.stringLiteral(port.name()))

    def loader(self):
        return jinja2.PackageLoader(__package__)

    def operations(self):
        for op in self.idl.operations():
            args = []
            returns = []
            if op.returnType.kind() != CORBA.tk_void:
                returns.append(str(op.returnType))
            for param in op.params:
                if param.direction in ('in', 'inout'):
                    args.append(param.name)
                if param.direction in ('inout', 'out'):
                    returns.append(str(param.paramType))
            yield {'name': op.name,
                   'args': args,
                   'returns': returns}
        for attr in self.idl.attributes():
            yield {'name': '_get_'+attr.name,
                   'args': [],
                   'returns': [str(attr.attrType)]}
            if not attr.readonly:
                yield {'name': '_set_'+attr.name,
                       'args': ['data'],
                       'returns': []}

    def _implementation(self):
        return self.__template
