import jinja2

from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.lang import cpp
from redhawk.codegen.jinja.ports import PortFactory
from redhawk.codegen.jinja.cpp import CppTemplate

from generator import CppPortGenerator

_elementTypes = {
    'dataFile':      'char',
    'dataXML':       'char',
    'dataChar':      'char',
    'dataDouble':    'CORBA::Double',
    'dataFloat':     'CORBA::Float',
    'dataLong':      'CORBA::Long',
    'dataLongLong':  'CORBA::LongLong',
    'dataOctet':     'unsigned char',
    'dataShort':     'CORBA::Short',
    'dataUlong':     'CORBA::ULong',
    'dataUlongLong': 'CORBA::ULongLong',
    'dataUshort':    'CORBA::UShort'
}

def sequenceType(interface):
    if interface == 'dataOctet':
        return 'CF::OctetSequence'
    elif interface in ('dataFile', 'dataXML'):
        return 'char *'
    else:
        return 'PortTypes::'+interface[4:]+'Sequence'

class BulkioPortFactory(PortFactory):
    NAMESPACE = 'BULKIO'

    def match(self, port):
        return IDLInterface(port.repid()).namespace() == self.NAMESPACE

    def generator(self, port):
        interface = IDLInterface(port.repid()).interface()
        return BulkioPortGenerator(port)

class BulkioPortGenerator(CppPortGenerator):

    def className(self):
        return "bulkio::" + self.templateClass()

    def templateClass(self):
        if self.direction == 'uses':
            porttype = 'Out'
        else:
            porttype = 'In'
        interface = self.interface[1:][3:]
        #If interface is unsigned need to make sure next character is
        #upper case to conform with bulkio base classes
        if interface[0] == "U":
            porttype += interface[0] + interface[1].upper() + interface[2:] + 'Port'
        else:
            porttype += interface + 'Port'
        return porttype

    def _ctorArgs(self, name):
        return [cpp.stringLiteral(name)]

    def elementType(self):
        return _elementTypes[self.interface]

    def sequenceType(self):
        return sequenceType(self.interface)

    def loader(self):
        return jinja2.PackageLoader(__package__)

