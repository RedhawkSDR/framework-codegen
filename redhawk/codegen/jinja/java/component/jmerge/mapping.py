from redhawk.codegen.lang import java
from redhawk.codegen.model.softwarecomponent import ComponentTypes
from redhawk.codegen.lang.idl import IDLInterface

from redhawk.codegen.jinja.mapping import ComponentMapper

class PullComponentMapper(ComponentMapper):
    def __init__(self, package):
        self.package = package

    def _mapComponent(self, softpkg):
        javacomp = {}
        javacomp['package'] = self.package
        userclass = softpkg.name()
        javacomp['userclass'] = {'name': userclass,
                                 'file': userclass+'.java'}
        javacomp['superclass'] = self.superclass(softpkg)
        javacomp['mainclass'] = java.qualifiedName(userclass, self.package)
        javacomp['jarfile'] = softpkg.name() + '.jar'
        javacomp['interfacedeps'] = list(self.getInterfaceDependencies(softpkg))
        javacomp['interfacejars'] = self.getInterfaceJars(softpkg)
        javacomp['hasbulkio'] = self.hasBulkioPorts(softpkg)
        return javacomp

    def getInterfaceDependencies(self, softpkg):
        for namespace in self.getInterfaceNamespaces(softpkg):
            if namespace == 'BULKIO':
                yield 'bulkio >= 1.0 bulkioInterfaces >= 1.9'
            elif namespace == 'REDHAWK':
                yield 'redhawkInterfaces >= 1.2.0'
            else:
                yield namespace.lower()+'Interfaces'

    def getInterfaceJars(self, softpkg):
        jars = [ns+'Interfaces.jar' for ns in self.getInterfaceNamespaces(softpkg)]
        jars.append('bulkio.jar')
        return jars

    def superclass(self, softpkg):
        if softpkg.type() == ComponentTypes.RESOURCE:
            name = 'Resource'
            artifactType = 'component'
        elif softpkg.type() == ComponentTypes.DEVICE:
            name = 'Device'
            artifactType = 'device'
        elif softpkg.type() == ComponentTypes.LOADABLEDEVICE:
            # NOTE: If java gets support for Loadable Devices, this needs to change
            name = 'Device'
            artifactType = 'device'
        elif softpkg.type() == ComponentTypes.EXECUTABLEDEVICE:
            # NOTE: If java gets support for Executable Devices, this needs to change
            name = 'Device'
            artifactType = 'device'
        else:
            raise ValueError, 'Unsupported software component type', softpkg.type()
        return {'name': name,
                'artifactType': artifactType}

    def hasBulkioPorts(self, softpkg):
        for port in softpkg.ports():
            if 'BULKIO' in port.repid():
                return True
        return False
