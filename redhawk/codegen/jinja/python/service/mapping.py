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

from redhawk.codegen.lang import python
from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.jinja.mapping import ComponentMapper

class ServiceMapper(ComponentMapper):
    def _mapComponent(self, softpkg):
        pycomp = {}
        pycomp['userclass'] = self.userClass(softpkg)
        idl = IDLInterface(softpkg.descriptor().repid().repid)
        pycomp['interface'] = idl.interface()
        pycomp['operations'] = idl.operations()
        pycomp['attributes'] = idl.attributes()
        module = python.idlModule(idl.namespace())
        poamod = python.poaModule(idl.namespace())
        pycomp['imports'] = (module, poamod)
        pycomp['baseclass'] = poamod.split('.')[-1] + '.' + idl.interface()
        
        return pycomp

    @staticmethod
    def userClass(softpkg):
        softpkg_base_name = softpkg.name()
        if softpkg.name().find('.') != -1:
            softpkg_base_name = softpkg.name().split('.')[-1]
        return {'name'  : softpkg_base_name,
                'file'  : softpkg_base_name+'.py'}
        
