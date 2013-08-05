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
        pycomp.update(self.getNamespace(idl))
        
        return pycomp

    @staticmethod
    def userClass(softpkg):
        return {'name'  : softpkg.name(),
                'file'  : softpkg.name()+'.py'}

    def getNamespace(self, idl):
        if idl.namespace().startswith('omg.org'):
            return {'imports': 'omniORB.COS',
                    'namespace': idl.namespace().split('/')[1] }
        elif idl.namespace().startswith('BULKIO'):
            return {'imports': 'bulkio.bulkioInterfaces',
                    'namespace': idl.namespace() }
        elif idl.namespace().startswith('CF'):
            return {'imports': 'ossie.cf',
                    'namespace': idl.namespace() }
        else:
            # Assume custom IDL
            return {'imports': 'redhawk.' + idl.namespace().lower() + 'Interfaces',
                    'namespace': idl.namespace() }
        
