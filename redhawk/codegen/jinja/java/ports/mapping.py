from redhawk.codegen.lang import java

from redhawk.codegen.jinja.mapping import PortMapper

class JavaPortMapper(PortMapper):
    def _mapPort(self, port, generator):
        javaport = {}
        javaport['javaname'] = java.identifier('port_'+port.name())
        javaport['javatype'] = generator.className()
        javaport['constructor'] = generator.constructor(port.name())
        return javaport
