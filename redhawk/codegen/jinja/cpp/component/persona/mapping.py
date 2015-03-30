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

class PersonaComponentMapper(PullComponentMapper):
    def _mapComponent(self, softpkg):
        cppcomp = PullComponentMapper._mapComponent(self, softpkg)
        cppcomp['reprogclass'] = self.reprogClass(softpkg)
        return cppcomp
    
    @staticmethod
    def reprogClass(softpkg):
        softpkg_base_name = softpkg.name()
        if softpkg.name().find('.') != -1:
            softpkg_base_name = softpkg.name().split('.')[-1]
        reprogclass = softpkg_base_name + '_persona_base'
        return {'name'  : reprogclass,
                'header': reprogclass+'.h',
                'file'  : reprogclass+'.cpp'}
