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
from redhawk.codegen.lang import python
from redhawk.codegen.jinja.ports import PortFactory
from redhawk.codegen.jinja.python import PythonTemplate

from generator import PythonPortGenerator

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

_elementTypes = {
    'dataFile':      'c', # NB: dataFile tracks statistics by character
    'dataXML':       'c', # NB: dataXML tracks statistics by character
    'dataChar':      'c',
    'dataDouble':    'd',
    'dataFloat':     'f',
    'dataLong':      'i',
    'dataLongLong':  'l',
    'dataOctet':     'B',
    'dataShort':     'h',
    'dataUlong':     'I',
    'dataUlongLong': 'L',
    'dataUshort':    'H'
}

class BulkioPortFactory(PortFactory):
    NAMESPACE = 'BULKIO'

    def match(self, port):
        return IDLInterface(port.repid()).namespace() == self.NAMESPACE
    
    def generator(self, port):
        interface = IDLInterface(port.repid()).interface()
        if port.isUses():
            return BulkioUsesGenerator(port)
        else:
            return BulkioProvidesGenerator(port)

class BulkioPortGenerator(PythonPortGenerator):
    def className(self):
        return "bulkio." + self.templateClass()

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

    def loader(self):
        return jinja2.PackageLoader(__package__)

    def elementType(self):
        return _elementTypes[self.interface]

    def dataParameterName(self):
        if self.interface == 'dataXML':
            return 'xml_string'
        elif self.interface == 'dataFile':
            return 'URL'
        else:
            return 'data'

class BulkioProvidesGenerator(BulkioPortGenerator):

    def _ctorArgs(self, port):
        if port.name().lower().find('sdds') == -1 :
            return (python.stringLiteral(port.name()), 'maxsize=self.DEFAULT_QUEUE_SIZE')
        else:
            return (python.stringLiteral(port.name()) )

class BulkioUsesGenerator(BulkioPortGenerator):

    def _ctorArgs(self, port):
        return ([str(python.stringLiteral((port.name())))])

    def poaClass(self):
        return 'bulkio.BULKIO__POA.UsesPortStatisticsProvider'

