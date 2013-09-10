from redhawk.codegen.lang import java
from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.jinja.mapping import ComponentMapper
from redhawk.codegen.jinja.java.ports.generic import *
from redhawk.codegen.model.softwarecomponent import ComponentTypes

class ServiceMapper(ComponentMapper):
    def __init__(self, package):
        self.package = package

    def _mapComponent(self, softpkg):
        javacomp = {}
        idl = IDLInterface(softpkg.descriptor().repid().repid)
        javacomp['interface'] = idl.interface()
        javacomp['operations'] = self.operations(idl)
        javacomp['attributes'] = self.attributes(idl)
        javacomp.update(self.getNamespace(idl))
       
        javacomp['package'] = self.package
        userclass = softpkg.name()
        baseclass = userclass + '_base'
        javacomp['baseclass'] = {'name': baseclass,
                                 'file': baseclass+'.java'}
        javacomp['userclass'] = {'name': userclass,
                                 'file': userclass+'.java'}
        javacomp['superclass'] = self.superclass(softpkg)
        javacomp['mainclass'] = java.qualifiedName(userclass, self.package)
        javacomp['jarfile'] = softpkg.name() + '.jar'
        javacomp['interfacedeps'] = list(self.getInterfaceDependencies(softpkg))
        javacomp['interfacejars'] = self.getInterfaceJars(softpkg)
        return javacomp

    def getInterfaceDependencies(self, softpkg):
        for namespace in self.getInterfaceNamespaces(softpkg):
            if namespace == 'BULKIO':
                yield 'bulkio >= 1.0 bulkioInterfaces >= 1.9'
            elif namespace == 'REDHAWK':
                yield 'redhawkInterfaces >= 1.2.0'
            else:
                yield namespace.lower()+'Interfaces'

    def getInterfaceJars(self, softpkg):
        jars = [ns+'Interfaces.jar' for ns in self.getInterfaceNamespaces(softpkg)]
        jars.append('bulkio.jar')
        return jars

    def superclass(self, softpkg):
        if softpkg.type() == ComponentTypes.SERVICE:
            name = 'Service'
        else:
            raise ValueError, 'Unsupported software component type', softpkg.type()
        return {'name': name}

    def getNamespace(self, idl):
        if idl.namespace().startswith('omg.org'):
            return {'imports': 'org.omg.',
                    'namespace': idl.namespace().split('/')[1] }
        else:
            return {'imports': '',
                    'namespace': idl.namespace() }

    def operations(self, idl):
        ops = []
        for op in idl.operations():
            ops.append({'name': op.name,
                   'arglist': ', '.join('%s %s' % (paramType(p), p.name) for p in op.params),
                   'argnames': [p.name for p in op.params],
                   'throws': ', '.join('%s%s' % (self.getNamespace(idl)['imports'], baseType(r)) for r in op.raises),
                   'returns': baseType(op.returnType)})
        return ops
        
    def attributes(self, idl):
        attrs = []
        for attr in idl.attributes():
            attrs.append({'name': attr.name,
                     'readonly': attr.readonly,
                     'type': baseType(attr.attrType)})
        return attrs

