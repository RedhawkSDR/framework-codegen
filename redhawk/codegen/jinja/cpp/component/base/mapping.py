from redhawk.codegen.jinja.mapping import ComponentMapper

class BaseComponentMapper(ComponentMapper):
    def _mapComponent(self, softpkg):
        cppcomp = {}
        cppcomp['userclass'] = { 'name'  : softpkg.name()+'_i',
                                 'header': softpkg.name()+'.h' }
        cppcomp['interfacedeps'] = tuple(self.getInterfaceDependencies(softpkg))
        return cppcomp

    def getInterfaceDependencies(self, softpkg):
        for namespace in self.getInterfaceNamespaces(softpkg):
            if namespace == 'BULKIO':
                yield 'bulkio >= 1.0 bulkioInterfaces >= 1.9'
            elif namespace == 'REDHAWK':
                yield 'redhawkInterfaces >= 1.2.0'
            else:
                yield namespace.lower()+'Interfaces'
