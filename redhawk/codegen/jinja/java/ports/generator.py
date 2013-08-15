from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.jinja.ports import PortGenerator

class JavaPortGenerator(PortGenerator):
    def __eq__(self, other):
        return self.className() == other.className()

    def className(self):
        porttype = '%s_%s' % (self.namespace, self.interface)
        if self.direction == 'uses':
            porttype += 'OutPort'
        else:
            porttype += 'InPort'
        return porttype

    def _basename(self):
        return '.'.join((self.namespace, self.interface))

    def interfaceClass(self):
        return self._basename() + 'Operations'

    def helperClass(self):
        return self._basename() + 'Helper'

    def poaClass(self):
        return self._basename() + 'POA'

    def _ctorArgs(self, name):
        return tuple()

    def constructor(self, name):
        return '%s(%s)' % (self.className(), ', '.join(self._ctorArgs(name)))

class BuiltinJavaPort(JavaPortGenerator):
    def __init__(self, javaclass, port):
        JavaPortGenerator.__init__(self, port)
        self.package, self.__name = javaclass.rsplit('.', 1)

    def className(self):
        return self.__name
