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

from redhawk.codegen.jinja.ports import PortFactoryList
from redhawk.codegen.jinja.java.ports.generic import GenericPortFactory
from redhawk.codegen.jinja.java.ports.bulkio import BulkioPortFactory
from redhawk.codegen.jinja.java.ports.event import PropertyEventPortGenerator
from redhawk.codegen.jinja.java.ports.message import MessagePortFactory

class PullPortFactory(PortFactoryList):
    def __init__(self):
        factories = (BulkioPortFactory(), PropertyEventPortGenerator, MessagePortFactory(), GenericPortFactory())
        super(PullPortFactory,self).__init__(*factories)
