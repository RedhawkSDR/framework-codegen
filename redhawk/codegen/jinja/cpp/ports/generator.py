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

from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.jinja.ports import PortGenerator

class CppPortGenerator(PortGenerator):
    def __init__(self, port):
        PortGenerator.__init__(self, port)
        self._header = None

    def __eq__(self, other):
        return self.className() == other.className()

    def className(self):
        porttype = '%s_%s' % (self.namespace, self.interface)
        if self.direction == 'uses':
            porttype += '_Out_i'
        else:
            porttype += '_In_i'
        return porttype

    def interfaceClass(self):
        return '::'.join((self.namespace, self.interface))

    def header(self):
        return self._header

    def setHeader(self, header):
        if not self.hasDeclaration():
            raise AssertionError('Cannot change header for non-generated ports')
        self._header = header

    def dependencies(self):
        return tuple()

    def _ctorArgs(self, name):
        return tuple()

    def hasStart(self):
        return self.start() is not None

    def start(self):
        return None

    def hasStop(self):
        return self.stop() is not None

    def stop(self):
        return None

    def constructor(self, name):
        return '%s(%s)' % (self.className(), ', '.join(self._ctorArgs(name)))

    def _declaration(self):
        return None

    def hasDeclaration(self):
        return self._declaration() is not None

    def declaration(self):
        template = self._declaration()
        return self.get_template(template)
