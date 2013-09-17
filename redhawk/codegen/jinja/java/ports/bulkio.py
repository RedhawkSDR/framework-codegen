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
from redhawk.codegen.lang import java
from redhawk.codegen.jinja.ports import PortFactory
from redhawk.codegen.jinja.java import JavaTemplate

from generator import JavaPortGenerator

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

_elementTypes = {
    'dataXML':       'string', # NB: This is only used for the argument name in pushPacket
    'dataFile':      'string', # NB: This is only used for the argument name in pushPacket
    'dataChar':      java.Types.CHAR,
    'dataDouble':    java.Types.DOUBLE,
    'dataFloat':     java.Types.FLOAT,
    'dataLong':      java.Types.INT,
    'dataLongLong':  java.Types.LONG,
    'dataOctet':     java.Types.BYTE,
    'dataShort':     java.Types.SHORT,
    'dataUlong':     java.Types.INT,
    'dataUlongLong': java.Types.LONG,
    'dataUshort':    java.Types.SHORT
}

def elementType(interface):
    return _elementTypes[interface]

def sequenceType(interface):
    if interface in ('dataFile', 'dataXML'):
        return 'String'
    else:
        return elementType(interface) + '[]'


class BulkioPortFactory(PortFactory):
    NAMESPACE = 'BULKIO'

    def match(self, port):
        return IDLInterface(port.repid()).namespace() == self.NAMESPACE

    def generator(self, port):
        interface = IDLInterface(port.repid()).interface()
        return BulkioPortGenerator(port)

class BulkioPortGenerator(JavaPortGenerator):
    def __init__(self, port):
        super(BulkioPortGenerator,self).__init__(port)

    def className(self):
        return self.templateClass()

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
        return [java.stringLiteral(name)]

    def elementType(self):
        return elementType(self.interface)

    def sequenceType(self):
        return sequenceType(self.interface)

    def _jnibasename(self):
        return '.'.join((self.namespace, 'jni', self.interface))

    def helperClass(self):
        return self._jnibasename() + 'Helper'

    def poaClass(self):
        return self._jnibasename() + 'POA'

    def loader(self):
        return jinja2.PackageLoader(__package__)
