from redhawk.codegen.lang import python

from redhawk.codegen.jinja.mapping import PortMapper

class PythonPortMapper(PortMapper):
    def _mapPort(self, port, generator):
        pyport = {}
        pyport['pyname'] = python.identifier('port_'+port.name())
        pyport['constructor'] = generator.constructor(port)
        return pyport
