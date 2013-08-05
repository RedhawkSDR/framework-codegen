from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.jinja.ports import PortGenerator

class PythonPortGenerator(PortGenerator):
    def __eq__(self, other):
        return self.className() == other.className()

    def className(self):
        return self.templateClass() + '_i'

    def templateClass(self):
        interface = self.interface[0].upper() + self.interface[1:]
        porttype = 'Port' + self.namespace + interface
        if self.direction == 'uses':
            porttype += 'Out'
        else:
            porttype += 'In'
        return porttype

    def attributeClass(self):
        return self.direction+'port'

    def imports(self):
        return []

    def corbaClass(self):
        return self.namespace + '.' + self.interface

    def poaClass(self):
        if self.direction == 'uses':
            return 'CF__POA.Port'
        else:
            return self.namespace + '__POA.' + self.interface

    def _ctorArgs(self, port):
        return []

    def constructor(self, port):
        return '%s(%s)' % (self.className(), ', '.join(self._ctorArgs(port)))

class builtinport(object):
    def __init__(self, pyclass):
        self.package, self.name = pyclass.rsplit('.', 1)

    def __call__(self, generator):
        imports = 'from %s import %s' % (self.package, self.name)
        generator.imports = lambda x: (imports,)
        generator.className = lambda x: self.name
        return generator
