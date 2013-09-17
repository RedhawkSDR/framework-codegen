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

from redhawk.codegen.lang import cpp
from redhawk.codegen.jinja.cpp import CppTemplate

from generator import CppPortGenerator

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

class MessagePortGenerator(CppPortGenerator):
    REPID = 'IDL:ExtendedEvent/MessageEvent:1.0'

    @classmethod
    def match(cls, port):
        return (port.repid() == cls.REPID)

    @classmethod
    def generator(cls, port):
        if port.isProvides():
            return MessageConsumerPortGenerator(port)
        else:
            return MessageSupplierPortGenerator(port)

    def _ctorArgs(self, name):
        return [cpp.stringLiteral(name)]

class MessageConsumerPortGenerator(MessagePortGenerator):
    def headers(self):
        return ('<ossie/MessageInterface.h>',)

    def className(self):
        return 'MessageConsumerPort'

class MessageSupplierPortGenerator(MessagePortGenerator):

    def headers(self):
        return (['<ossie/MessageInterface.h>'])

    def loader(self):
        return jinja2.PackageLoader(__package__)

    def _declaration(self):
        return CppTemplate('message.h')
