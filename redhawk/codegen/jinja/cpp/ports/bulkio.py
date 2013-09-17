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

import jinja2

from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.lang import cpp
from redhawk.codegen.jinja.ports import PortFactory
from redhawk.codegen.jinja.cpp import CppTemplate

from generator import CppPortGenerator

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

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
    def start(self):
        if self.direction == 'provides' and self.templateClass() !="InSDDSPort":
            return 'unblock()'
        else:
            return None

    def stop(self):
        if self.direction == 'provides' and self.templateClass() !="InSDDSPort":
            return 'block()'
        else:
            return None

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

