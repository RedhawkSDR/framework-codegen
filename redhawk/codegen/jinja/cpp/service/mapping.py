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
from redhawk.codegen.jinja.mapping import ComponentMapper
from redhawk.codegen.jinja.cpp.ports import generic

class ServiceMapper(ComponentMapper):
    def _mapComponent(self, softpkg):
        cppcomp = {}
        idl = IDLInterface(softpkg.descriptor().repid().repid)
        cppcomp['baseclass'] = self.baseClass(softpkg)
        cppcomp['userclass'] = self.userClass(softpkg)
        cppcomp['superclass'] = self.superClass(softpkg)
        cppcomp['interfacedeps'] = tuple(self.getInterfaceDependencies(softpkg))
        idl = IDLInterface(softpkg.descriptor().repid().repid)
        cppcomp['namespace'] = self.getNamespace(idl)
        cppcomp['interface'] = idl.interface()
        cppcomp['operations'] = self.getOperations(idl)
        cppcomp['header'] = self.getHeader(idl)
        return cppcomp

    @staticmethod
    def userClass(softpkg):
        return {'name'  : softpkg.name()+'_i',
                'header': softpkg.name()+'.h',
                'file'  : softpkg.name()+'.cpp'}

    @staticmethod
    def baseClass(softpkg):
        baseclass = softpkg.name() + '_base'
        return {'name'  : baseclass,
                'header': baseclass+'.h',
                'file'  : baseclass+'.cpp'}

    @staticmethod
    def superClass(softpkg):
        name = 'Service_impl'
        return {'name': name,
                'header': '<ossie/'+name+'.h>'}

    def getInterfaceDependencies(self, softpkg):
        for namespace in self.getInterfaceNamespaces(softpkg):
            if namespace == 'BULKIO':
                yield 'bulkio >= 1.0 bulkioInterfaces >= 1.9'
            elif namespace == 'REDHAWK':
                yield 'redhawkInterfaces >= 1.2.0'
            else:
                yield namespace.lower()+'Interfaces'

    def getOperations(self, idl):
        operations = []
        for op in idl.operations():
            operations.append({'name': op.name,
                   'arglist': ', '.join('%s %s' % (generic.paramType(p), p.name) for p in op.params),
                   'argnames': ', '.join(p.name for p in op.params),
                   'returns': generic.baseReturnType(op.returnType)})
        for attr in idl.attributes():
            operations.append({'name': attr.name,
                   'arglist': '',
                   'argnames': '',
                   'returns': generic.baseReturnType(attr.attrType)})
            if not attr.readonly:
                operations.append({'name': attr.name,
                       'arglist': generic.baseType(attr.attrType) + ' data',
                       'argnames': 'data',
                       'returns': 'void'})
        return operations

    def getNamespace(self, idl):
        if idl.namespace().startswith('omg.org'):
            return idl.namespace().split('/')[1]
        elif idl.namespace().startswith('BULKIO'):
            return idl.namespace()
        elif idl.namespace().startswith('CF'):
            return idl.namespace()
        else:
            # Assume custom IDL
            return idl.namespace()

    def getHeader(self, idl):
        if idl.namespace().startswith('omg.org'):
            retidl = idl.idl().fullpath.split('/')[-2]+'/'+idl.idl().fullpath.split('/')[-1]
            retidl = retidl.replace('.idl','.hh')
            return retidl
        elif idl.namespace().startswith('BULKIO'):
            retidl = idl.idl().fullpath.split('/')[-2]+'/'+idl.idl().fullpath.split('/')[-1]
            retidl = retidl.replace('.idl','.h')
            return retidl
        elif idl.namespace().startswith('CF'):
            retidl = idl.idl().fullpath.split('/')[-2]+'/'+idl.idl().fullpath.split('/')[-1]
            retidl = retidl.replace('.idl','.h')
            return retidl
        else:
            # Assume custom IDL
            retidl = idl.idl().fullpath.split('/')[-2]+'/'+idl.idl().fullpath.split('/')[-1]
            retidl = retidl.replace('.idl','.h')
            return retidl
