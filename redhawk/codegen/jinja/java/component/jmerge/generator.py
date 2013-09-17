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

import os

from redhawk.codegen import utils

from redhawk.codegen.jinja.loader import CodegenLoader
from redhawk.codegen.jinja.common import ShellTemplate, AutomakeTemplate, AutoconfTemplate
from redhawk.codegen.jinja.java import JavaCodeGenerator, JavaTemplate
from redhawk.codegen.jinja.java.properties import JavaPropertyMapper
from redhawk.codegen.jinja.java.ports import JavaPortMapper

from mapping import PullComponentMapper
from portfactory import PullPortFactory

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

loader = CodegenLoader(__package__,
                       {'base': 'redhawk.codegen.jinja.java.component.base',
                        'common': 'redhawk.codegen.jinja.common'})

class PullComponentGenerator(JavaCodeGenerator):
    # Need to keep use_jni and auto_start to handle legacy options
    def parseopts (self, java_package='',use_jni=True, auto_start=True):
        self.package = java_package

    def loader(self, component):
        return loader

    def componentMapper(self):
        return PullComponentMapper(self.package)

    def propertyMapper(self):
        return JavaPropertyMapper()

    def portMapper(self):
        return JavaPortMapper()

    def portFactory(self):
        return PullPortFactory()

    def templates(self, component):
        # Put generated Java files in "src" subdirectory, followed by their
        # package path.
        pkgpath = os.path.join('src', *component['package'].split('.'))
        mainfile = component['userclass']['file']
        templates = [
            JavaTemplate('resource.java', os.path.join(pkgpath, mainfile)),
            AutomakeTemplate('base/Makefile.am'),
            AutoconfTemplate('base/configure.ac'),
            ShellTemplate('base/startJava.sh'),
            ShellTemplate('common/reconf')
        ]

        portpkg = component['package'] + '.' + 'ports'
        portpkgpath = os.path.join(pkgpath, 'ports')
        for generator in component['portgenerators']:
            if not generator.hasImplementation():
                continue
            generator.package = portpkg
            template = generator.implementation()
            filename = os.path.join(portpkgpath, generator.className()+'.java')
            context = {'portgenerator': generator}
            templates.append(JavaTemplate(template, filename, portpkg, context))

        return templates
