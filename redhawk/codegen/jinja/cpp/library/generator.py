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

import jinja2

from redhawk.codegen.jinja.loader import CodegenLoader
from redhawk.codegen.jinja.common import ShellTemplate, AutomakeTemplate, AutoconfTemplate, PkgconfigTemplate
from redhawk.codegen.jinja.cpp import CppCodeGenerator, CppTemplate
from redhawk.codegen.jinja.mapping import SoftpkgMapper

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

loader = CodegenLoader(__package__,
                       {'common': 'redhawk.codegen.jinja.common',
                        'base':   'redhawk.codegen.jinja.cpp.component.base'})

class LibraryMapper(SoftpkgMapper):
    def _mapComponent(self, softpkg):
        cpplib = {}
        cpplib['libname'] = 'lib'+softpkg.name()+'.la'
        cpplib['incfile'] = softpkg.name() + '.h'
        cpplib['srcfile'] = softpkg.name() + '.cpp'
        cpplib['pcfile'] = softpkg.name() + '.pc'
        return cpplib

class LibraryGenerator(CppCodeGenerator):
    def parseopts(self, includedir='include', sourcedir='src'):
        self.includedir = includedir
        self.sourcedir = sourcedir

    def loader(self, component):
        return loader

    def componentMapper(self):
        return LibraryMapper()

    def propertyMapper(self):
        return None

    def portMapper(self):
        return None

    def templates(self, library):
        userHeader = os.path.join(self.includedir, library['incfile'])
        userSource = os.path.join(self.sourcedir, library['srcfile'])

        templates = [
            CppTemplate('library.h', userHeader, userfile=True),
            CppTemplate('library.cpp', userSource, userfile=True),
            AutomakeTemplate('Makefile.am'),
            AutomakeTemplate('base/Makefile.am.ide', userfile=True),
            AutoconfTemplate('configure.ac'),
            ShellTemplate('base/build.sh'),
            ShellTemplate('common/reconf'),
            PkgconfigTemplate('library.pc.in', library['pcfile']+'.in')
        ]

        return templates
