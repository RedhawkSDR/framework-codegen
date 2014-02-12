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

from redhawk.codegen.jinja.loader import CodegenLoader
from redhawk.codegen.jinja.cpp.component.pull import PullComponentGenerator
from redhawk.codegen.jinja.cpp.ports import FEIPortFactory
from redhawk.codegen.jinja.cpp import CppTemplate
from redhawk.codegen.jinja.common import ShellTemplate, AutomakeTemplate, AutoconfTemplate

from mapping import FrontendComponentMapper, FrontendPropertyMapper

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

loader = CodegenLoader(__package__,
                       {'common'         : 'redhawk.codegen.jinja.common',
                        'base'           : 'redhawk.codegen.jinja.cpp.component.base',
                        'pull'           : 'redhawk.codegen.jinja.cpp.component.pull',
                        'properties'     : 'redhawk.codegen.jinja.cpp.properties'})

class FrontendComponentGenerator(PullComponentGenerator):
    def loader(self, component):
        return loader

    def componentMapper(self):
        return FrontendComponentMapper()

    def propertyMapper(self):
        return FrontendPropertyMapper()

    def portFactory(self):
        return FEIPortFactory()

    def templates(self, component):
        templates = [
            CppTemplate('base/main.cpp'),
            AutomakeTemplate('base/Makefile.am'),
            AutomakeTemplate('base/Makefile.am.ide', userfile=True),
            AutoconfTemplate('base/configure.ac'),
            ShellTemplate('base/build.sh'),
            ShellTemplate('common/reconf'),
            CppTemplate('resource.cpp', component['userclass']['file'], userfile=True),
            CppTemplate('resource.h', component['userclass']['header'], userfile=True),
            CppTemplate('resource_base.cpp', component['baseclass']['file']),
            CppTemplate('resource_base.h', component['baseclass']['header']),
            CppTemplate('template_impl.cpp')
        ]

        for gen in component['portgenerators']:
            # Need to include port_impl if a non-bulkio port exists
            if str(type(gen)).find("BulkioPortGenerator") == -1:
                templates.append(CppTemplate('pull/port_impl.cpp'))
                templates.append(CppTemplate('pull/port_impl.h'))
                break

        if component['structdefs']:
            templates.append(CppTemplate('struct_props.h'))

        return templates
