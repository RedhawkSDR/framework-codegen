#
# This file is protected by Copyright. Please refer to the COPYRIGHT file
# distributed with this source distribution.
#
# This file is part of REDHAWK core.
#
# REDHAWK core is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# REDHAWK core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

from redhawk.codegen.model.softwarecomponent import ComponentTypes
from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.jinja.cpp.component.pull.mapping import PullComponentMapper
from redhawk.codegen.jinja.cpp.properties.mapping import CppPropertyMapper

class FrontendComponentMapper(PullComponentMapper):
    def _mapComponent(self, softpkg):
        cppcomp = {}
        cppcomp['baseclass'] = self.baseClass(softpkg)
        cppcomp['userclass'] = self.userClass(softpkg)
        cppcomp['superclasses'] = self.superClasses(softpkg)
        cppcomp['interfacedeps'] = tuple(self.getInterfaceDependencies(softpkg))
        cppcomp['hasbulkio'] = self.hasBulkioPorts(softpkg)
        cppcomp['hasfrontend'] = self.hasFrontendPorts(softpkg)
        cppcomp['hasfrontendprovides'] = self.hasFrontendProvidesPorts(softpkg)
        cppcomp['isafrontendtuner'] = self.isAFrontendTuner(softpkg)
        cppcomp['hasfrontendtunerprovides'] = self.hasFrontendTunerProvidesPorts(softpkg)
        cppcomp['hasdigitaltunerprovides'] = self.hasDigitalTunerProvidesPorts(softpkg)
        cppcomp['hasanalogtunerprovides'] = self.hasAnalogTunerProvidesPorts(softpkg)
        cppcomp['hasmultioutport'] = self.hasMultioutPort(softpkg)
        cppcomp['softpkgdeps'] = self.softPkgDeps(softpkg, format='deps')
        cppcomp['pkgconfigsoftpkgdeps'] = self.softPkgDeps(softpkg, format='pkgconfig')
        return cppcomp

    @staticmethod
    def superClasses(softpkg):
        hasDigitalTunerProvides = False
        hasAnalogTunerProvides = False
        hasFrontendTunerProvides = False
        hasRFInfoProvides = False
        hasRFSourceProvides = False
        hasGPSInfoProvides = False
        hasNavDataProvides = False
        if softpkg.type() == ComponentTypes.RESOURCE:
            name = 'Resource_impl'
        elif softpkg.type() == ComponentTypes.DEVICE:
            # If device contains FrontendInterfaces 
            #  FrontendTuner, DigitalTuner or AnalogTuner, have
            #  device inherit from FrontendTunerDevice 
            #  instead of Device_impl
            name = 'Device_impl'
            for port in softpkg.providesPorts():
                idl = IDLInterface(port.repid())
                if idl.namespace() == 'FRONTEND':
                    if idl.interface().find('DigitalTuner') != -1:
                        hasDigitalTunerProvides = True
                        name = 'frontend::FrontendTunerDevice<frontend_tuner_status_struct_struct>'
                    elif idl.interface().find('AnalogTuner') != -1:
                        hasAnalogTunerProvides = True
                        name = 'frontend::FrontendTunerDevice<frontend_tuner_status_struct_struct>'
                    elif idl.interface().find('FrontendTuner') != -1:
                        hasFrontendTunerProvides = True
                        name = 'frontend::FrontendTunerDevice<frontend_tuner_status_struct_struct>'
                    elif idl.interface().find('RFInfo') != -1:
                        hasRFInfoProvides = True
                    elif idl.interface().find('RFSource') != -1:
                        hasRFSourceProvides = True
                    elif idl.interface().find('GPS') != -1:
                        hasGPSInfoProvides = True
                    elif idl.interface().find('NavData') != -1:
                        hasNavDataProvides = True
            aggregate = 'virtual POA_CF::AggregatePlainDevice'
        elif softpkg.type() == ComponentTypes.LOADABLEDEVICE:
            name = 'LoadableDevice_impl'
            aggregate = 'virtual POA_CF::AggregateLoadableDevice'
        elif softpkg.type() == ComponentTypes.EXECUTABLEDEVICE:
            name = 'ExecutableDevice_impl'
            aggregate = 'virtual POA_CF::AggregateExecutableDevice'
        else:
            raise ValueError, 'Unsupported software component type', softpkg.type()

        if name == 'frontend::FrontendTunerDevice<frontend_tuner_status_struct_struct>':
            classes = [{'name': name, 'header': '<frontend/frontend.h>'}]
        else:
            classes = [{'name': name, 'header': '<ossie/'+name+'.h>'}]

        if hasDigitalTunerProvides == True:
            classes.append({'name': 'virtual frontend::digital_tuner_delegation', 'header': ''})
        if hasAnalogTunerProvides == True:
            classes.append({'name': 'virtual frontend::analog_tuner_delegation', 'header': ''})
        if hasFrontendTunerProvides == True:
            classes.append({'name': 'virtual frontend::frontend_tuner_delegation', 'header': ''})
        if hasRFInfoProvides == True:
            classes.append({'name': 'virtual frontend::rfinfo_delegation', 'header': ''})
        if hasRFSourceProvides == True:
            classes.append({'name': 'virtual frontend::rfsource_delegation', 'header': ''})
        if hasGPSInfoProvides == True:
            classes.append({'name': 'virtual frontend::gps_delegation', 'header': ''})
        if hasNavDataProvides == True:
            classes.append({'name': 'virtual frontend::nav_delegation', 'header': ''})

        if softpkg.descriptor().supports('IDL:CF/AggregateDevice:1.0'):
            classes.append({'name': aggregate, 'header': '<CF/AggregateDevices.h>'})
            classes.append({'name': 'AggregateDevice_impl', 'header': '<ossie/AggregateDevice_impl.h>'})

        return classes

    def hasFrontendPorts(self, softpkg):
        for port in softpkg.ports():
            if 'FRONTEND' in port.repid():
                return True
        return False

    def hasFrontendProvidesPorts(self, softpkg):
        for port in softpkg.providesPorts():
            if 'FRONTEND' in port.repid():
                return True
        return False

    def isAFrontendTuner(self,softpkg):
        return self.hasFrontendTunerProvidesPorts(softpkg) or \
               self.hasAnalogTunerProvidesPorts(softpkg) or \
               self.hasDigitalTunerProvidesPorts(softpkg)
                 

    def hasFrontendTunerProvidesPorts(self, softpkg):
        for port in softpkg.providesPorts():
            idl = IDLInterface(port.repid())
            if idl.namespace() == 'FRONTEND':
                if idl.interface().find('FrontendTuner') != -1:
                    return True
        return False

    def hasDigitalTunerProvidesPorts(self, softpkg):
        for port in softpkg.providesPorts():
            idl = IDLInterface(port.repid())
            if idl.namespace() == 'FRONTEND':
                if idl.interface().find('DigitalTuner') != -1:
                    return True
        return False

    def hasAnalogTunerProvidesPorts(self, softpkg):
        for port in softpkg.providesPorts():
            idl = IDLInterface(port.repid())
            if idl.namespace() == 'FRONTEND':
                if idl.interface().find('AnalogTuner') != -1:
                    return True
        return False

    def hasMultioutPort(self, softpkg):
        for prop in softpkg.getStructSequenceProperties():
            if prop.name() == "connectionTable" and  \
               prop.struct().name() == "connection_descriptor":
                foundConnectionName = False
                foundStreamId = False
                foundPortName = False
                for field in prop.struct().fields():
                    if field.name() == "connection_id":
                        foundConnectionName = True 
                    elif field.name() == "stream_id":
                        foundStreamId = True 
                    elif field.name() == "port_name":
                        foundPortName = True 
                if foundConnectionName == True and \
                   foundStreamId == True and \
                   foundPortName == True:
                    return True
        return False

    def hasBulkioPorts(self, softpkg):
        for port in softpkg.ports():
            if 'BULKIO' in port.repid():
                return True
        return False

class FrontendPropertyMapper(CppPropertyMapper):
    def _mapStruct(self, prop):
        propdict = super(FrontendPropertyMapper,self)._mapStruct(prop)
        propdict['basefields'] = []
        if prop.name() == "frontend_tuner_status_struct":
            # These fields are defined in the inherited base structs
            # so they won't need to be defined in the generated code
            if "tuner_type" not in propdict['basefields']:
                propdict['basefields'].append("tuner_type")
            if "allocation_id_csv" not in propdict['basefields']:
                propdict['basefields'].append("allocation_id_csv")
            if "center_frequency" not in propdict['basefields']:
                propdict['basefields'].append("center_frequency")
            if "bandwidth" not in propdict['basefields']:
                propdict['basefields'].append("bandwidth")
            if "sample_rate" not in propdict['basefields']:
                propdict['basefields'].append("sample_rate")
            if "enabled" not in propdict['basefields']:
                propdict['basefields'].append("enabled")
            if "group_id" not in propdict['basefields']:
                propdict['basefields'].append("group_id")
            if "rf_flow_id" not in propdict['basefields']:
                propdict['basefields'].append("rf_flow_id")
        return propdict

    def mapStructProperty(self, prop, fields):
        cppprop = self.mapProperty(prop)
        if prop.name() == "frontend_tuner_allocation" or \
           prop.name() == "frontend_listener_allocation":
            typename = "frontend::" + prop.name()+'_struct'
        else:
            typename = prop.name()+'_struct'
        cppprop['cpptype'] = typename
        cppprop['cppvalue'] = typename + '()'
        return cppprop

    def mapStructSequenceProperty(self, prop, structdef):
        cppprop = self.mapProperty(prop)
        if prop.name() == "frontend_tuner_allocation":
            cppprop['cpptype'] = 'std::vector<frontend_tuner_status_struct_struct>'
        else:
            cppprop['cpptype'] = 'std::vector<%s>' % structdef['cpptype']
        cppprop['cppvalues'] = [self.mapStructValue(structdef, value) for value in prop.value()]
        return cppprop

