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

from redhawk.codegen.jinja.mapping import ComponentMapper
import commands, os

class BaseComponentMapper(ComponentMapper):
    def _mapComponent(self, softpkg):
        cppcomp = {}
        cppcomp['userclass'] = { 'name'  : softpkg.name()+'_i',
                                 'header': softpkg.name()+'.h' }
        cppcomp['interfacedeps'] = tuple(self.getInterfaceDependencies(softpkg))
        cppcomp['softpkgdeps'] = self.softPkgDeps(softpkg, format='deps')
        cppcomp['pkgconfigsoftpkgdeps'] = self.softPkgDeps(softpkg, format='pkgconfig')
        return cppcomp

    def getInterfaceDependencies(self, softpkg):
        for namespace in self.getInterfaceNamespaces(softpkg):
            if namespace == 'BULKIO':
                yield 'bulkio >= 1.0 bulkioInterfaces >= 1.9'
            elif namespace == 'BURSTIO':
                yield 'burstio >= 1.8'
            elif namespace == 'REDHAWK':
                yield 'redhawkInterfaces >= 1.2.0'
            else:
                yield namespace.lower()+'Interfaces'

    def softPkgDeps(self, softpkg, format='deps'):
        deps = ''
        for dep in softpkg.getSoftPkgDeps():
            pc_filename = dep['localfile'][:dep['localfile'].rfind('/')]+'/lib/pkgconfig'
            status,output = commands.getstatusoutput('pkg-config '+os.getenv('SDRROOT')+'/dom'+pc_filename+'/'+dep['name']+'.pc'' --modversion')
            if status != 0:
                pc_filename = dep['localfile'][:dep['localfile'].rfind('/')]+'/lib64/pkgconfig'
                status,output = commands.getstatusoutput('pkg-config '+os.getenv('SDRROOT')+'/dom'+pc_filename+'/'+dep['name']+'.pc'' --modversion')
            if status == 0:
                if format == 'deps':
                    deps += dep['name']+' >= '+output+' '
                elif format == 'pkgconfig':
                    deps += '$SDRROOT/dom'+pc_filename+':'
        return deps
