import sys
from redhawk.codegen.model.softwarecomponent import ComponentTypes
from redhawk.codegen.lang.idl import IDLInterface

from redhawk.codegen.jinja.mapping import ComponentMapper

class PullComponentMapper(ComponentMapper):
    def _mapComponent(self, softpkg):
        pycomp = {}
        pycomp['baseclass'] = self.baseClass(softpkg)
        pycomp['userclass'] = self.userClass(softpkg)
        pycomp['superclass'] = self.superclass(softpkg)
        pycomp['poaclass'] = self.poaclass(softpkg)
        pycomp['interfacedeps'] = self.getInterfaceDependencies(softpkg)
        pycomp['hasbulkio'] = self.hasBulkioPorts(softpkg)
        return pycomp

    @staticmethod
    def userClass(softpkg):
        return {'name'  : softpkg.name()+'_i',
                'file'  : softpkg.name()+'.py'}

    @staticmethod
    def baseClass(softpkg):
        baseclass = softpkg.name() + '_base'
        return {'name'  : baseclass,
                'file'  : baseclass+'.py'}

    @staticmethod
    def superclass(softpkg):
        if softpkg.type() == ComponentTypes.RESOURCE:
            name = 'Resource'
            artifactType = 'component'
        elif softpkg.type() == ComponentTypes.DEVICE:
            name = 'Device'
            artifactType = 'device'
        elif softpkg.type() == ComponentTypes.LOADABLEDEVICE:
            name = 'LoadableDevice'
            artifactType = 'device'
        elif softpkg.type() == ComponentTypes.EXECUTABLEDEVICE:
            name = 'ExecutableDevice'
            artifactType = 'device'
        else:
            raise ValueError, 'Unsupported software component type', softpkg.type()
        return {'name': name,
                'artifactType': artifactType }

    @staticmethod
    def poaclass(softpkg):
        if softpkg.type() == ComponentTypes.RESOURCE:
            return 'CF__POA.Resource'
        elif softpkg.type() == ComponentTypes.DEVICE:
            return 'CF__POA.Device'
        elif softpkg.type() == ComponentTypes.LOADABLEDEVICE:
            return 'CF__POA.LoadableDevice'
        elif softpkg.type() == ComponentTypes.EXECUTABLEDEVICE:
            return 'CF__POA.ExecutableDevice'
        else:
            raise ValueError, 'Unsupported software component type', softpkg.type()

    def getInterfaceDependencies(self, softpkg):
        for namespace in self.getInterfaceNamespaces(softpkg):
            name = namespace.lower() + 'Interfaces'
            if namespace == 'BULKIO':
                package = 'bulkio'
                version = ' >= 1.8'
            elif namespace == 'REDHAWK':
                package = 'redhawk'
                version = ' >= 1.2'
            else:
                package = 'redhawk'
                version = ''
            yield {'name': name, 'module': package+'.'+name, 'version': version}

    def hasBulkioPorts(self, softpkg):
        for port in softpkg.ports():
            if 'BULKIO' in port.repid():
                return True
        return False

