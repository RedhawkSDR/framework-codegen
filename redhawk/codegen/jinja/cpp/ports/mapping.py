from redhawk.codegen.lang import cpp
from redhawk.codegen.jinja.mapping import PortMapper

class CppPortMapper(PortMapper):
    def _mapPort(self, port, generator):
        cppport = {}
        cppport['cppname'] = cpp.identifier(port.name())
        cppport['cpptype'] = generator.className()
        if generator.hasStart():
            cppport['start'] = generator.start()
        if generator.hasStop():
            cppport['stop'] = generator.stop()
        cppport['constructor'] = generator.constructor(port.name())
        cppport['headers'] = generator.headers()
        return cppport
