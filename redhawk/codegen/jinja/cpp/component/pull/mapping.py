from redhawk.codegen.model.softwarecomponent import ComponentTypes
from redhawk.codegen.lang.idl import IDLInterface

from redhawk.codegen.jinja.cpp.component.base import BaseComponentMapper

class PullComponentMapper(BaseComponentMapper):
    def _mapComponent(self, softpkg):
        cppcomp = {}
        cppcomp['baseclass'] = self.baseClass(softpkg)
        cppcomp['userclass'] = self.userClass(softpkg)
        cppcomp['superclasses'] = self.superClasses(softpkg)
        cppcomp['interfacedeps'] = tuple(self.getInterfaceDependencies(softpkg))
        cppcomp['hasbulkio'] = self.hasBulkioPorts(softpkg)
        return cppcomp

    @staticmethod
    def userClass(softpkg):
        return {'name'  : softpkg.name()+'_i',
                'header': softpkg.name()+'.h',
                'file'  : softpkg.name()+'.cpp'}

    @staticmethod
    def baseClass(softpkg):
        baseclass = softpkg.name() + '_base'
        return {'name'  : baseclass,
                'header': baseclass+'.h',
                'file'  : baseclass+'.cpp'}

    @staticmethod
    def superClasses(softpkg):
        if softpkg.type() == ComponentTypes.RESOURCE:
            name = 'Resource_impl'
        elif softpkg.type() == ComponentTypes.DEVICE:
            name = 'Device_impl'
            aggregate = 'virtual POA_CF::AggregatePlainDevice'
        elif softpkg.type() == ComponentTypes.LOADABLEDEVICE:
            name = 'LoadableDevice_impl'
            aggregate = 'virtual POA_CF::AggregateLoadableDevice'
        elif softpkg.type() == ComponentTypes.EXECUTABLEDEVICE:
            name = 'ExecutableDevice_impl'
            aggregate = 'virtual POA_CF::AggregateExecutableDevice'
        else:
            raise ValueError, 'Unsupported software component type', softpkg.type()
        classes = [{'name': name, 'header': '<ossie/'+name+'.h>'}]
        if softpkg.descriptor().supports('IDL:CF/AggregateDevice:1.0'):
            classes.append({'name': aggregate, 'header': '<CF/AggregateDevices.h>'})
            classes.append({'name': 'AggregateDevice_impl', 'header': '<ossie/AggregateDevice_impl.h>'})
        return classes

    def hasBulkioPorts(self, softpkg):
        for port in softpkg.ports():
            if 'BULKIO' in port.repid():
                return True
        return False

    def hasBulkioProvidesPorts(self, softpkg):
        for port in softpkg.providesPorts():
            if 'BULKIO' in port.repid():
                return True
        return False

    def hasProvidesPushPacket(self, softpkg):
        for port in softpkg.providesPorts():
            idl = IDLInterface(port.repid())
            if idl.namespace() == 'BULKIO' and idl.interface().startswith('data'):
                return True
        return False

    def hasSDDSInput(self, softpkg):
        for port in softpkg.providesPorts():
            if 'BULKIO/dataSDDS' in port.repid():
                return True
        return False
