from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.jinja.ports import PortGenerator

class CppPortGenerator(PortGenerator):
    def __eq__(self, other):
        return self.className() == other.className()

    def className(self):
        porttype = '%s_%s' % (self.namespace, self.interface)
        if self.direction == 'uses':
            porttype += '_Out_i'
        else:
            porttype += '_In_i'
        return porttype

    def interfaceClass(self):
        return '::'.join((self.namespace, self.interface))

    def headers(self):
        return tuple()

    def _ctorArgs(self, name):
        return tuple()

    def hasStart(self):
        return self.start() is not None

    def start(self):
        return None

    def hasStop(self):
        return self.stop() is not None

    def stop(self):
        return None

    def constructor(self, name):
        return '%s(%s)' % (self.className(), ', '.join(self._ctorArgs(name)))

    def _declaration(self):
        return None

    def hasDeclaration(self):
        return self._declaration() is not None

    def declaration(self):
        template = self._declaration()
        return self.get_template(template)
