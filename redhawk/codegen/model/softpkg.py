import os
import ossie.parsers

from redhawk.codegen.utils import strenum

import properties
from softwarecomponent import SoftwareComponent, ComponentTypes

class Implementation(object):
    def __init__(self, impl):
        self.__impl = impl

    def prfFile(self):
        if self.__impl.propertyfile:
            return self.__impl.propertyfile.localfile.name
        else:
            return None

    def identifier(self):
        return self.__impl.id_

    def entrypoint(self):
        return self.__impl.code.entrypoint

    def programminglanguage(self):
        return self.__impl.programminglanguage.name

class SoftPkg(object):
    def __init__(self, spdFile):
        self.__spdFile = os.path.basename(spdFile)
        self.__spd = ossie.parsers.spd.parse(spdFile)
        self.__impls = dict((impl.id_, Implementation(impl)) for impl in self.__spd.implementation)

        self.__path = os.path.dirname(spdFile)

        self.__scdFile = self.__spd.descriptor.localfile.name
        self.__desc = SoftwareComponent(os.path.join(self.__path, self.__scdFile))

        if self.__spd.get_propertyfile():
            self.__prfFile = self.__spd.propertyfile.localfile.name
            if os.path.exists(os.path.join(self.__path, self.__prfFile)):
                self.__props = properties.parse(os.path.join(self.__path, self.__prfFile))
            else:
                self.__props = []
        else:
            self.__props = []
            self.__prfFile = None

    def spdFile(self):
        return self.__spdFile

    def prfFile(self):
        return self.__prfFile

    def scdFile(self):
        return self.__scdFile

    def type(self):
        return self.__desc.type()

    def isDevice(self):
        return self.type() == ComponentTypes.DEVICE

    def descriptor(self):
        return self.__desc

    def name(self):
        return self.__spd.name

    def version(self):
        if not self.__spd.version:
            return '1.0.0'
        else:
            return self.__spd.version

    def hasDescription(self):
        return self.description() is not None

    def description(self):
        return self.__spd.description

    def usesPorts(self):
        return self.__desc.uses()

    def providesPorts(self):
        return self.__desc.provides()

    def ports(self):
        return self.__desc.ports()

    def properties(self):
        return self.__props

    def implementations(self):
        return self.__impls.values()

    def getImplementation(self, implId):
        return self.__impls[implId]

    def hasPorts(self):
        return len(self.ports()) > 0

    def hasProperties(self):
        return len(self.__props) > 0

    def hasStructProps(self):
        for prop in self.__props:
            if prop.isStruct():
                return True
        return False

    def getStructDefinitions(self):
        structdefs = [s for s in self.getStructProperties()]
        structdefs += [s.struct() for s in self.getStructSequenceProperties()]
        return structdefs

    def getSimpleProperties(self):
        return [p for p in self.__props if not p.isStruct() and not p.isSequence()]

    def getSimpleSequenceProperties(self):
        return [p for p in self.__props if not p.isStruct() and p.isSequence()]

    def getStructProperties(self):
        return [p for p in self.__props if p.isStruct() and not p.isSequence()]

    def getStructSequenceProperties(self):
        return [p for p in self.__props if p.isStruct() and p.isSequence()]

    def hasSDDSPort(self):
        for port in self.ports():
            if port.repid().find('BULKIO/dataSDDS'):
                return True
        return False

    def getSdrPath(self):
        comptype = self.type()
        if comptype == ComponentTypes.RESOURCE:
            return 'dom/components'
        elif comptype == ComponentTypes.DEVICE or comptype == ComponentTypes.LOADABLEDEVICE or comptype == ComponentTypes.EXECUTABLEDEVICE:
            return 'dev/devices'            
        elif comptype == ComponentTypes.SERVICE:
            return 'dev/services'
        raise ValueError, 'Unsupported software component type', comptype
