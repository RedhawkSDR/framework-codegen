import os

from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen.model.softwarecomponent import ComponentTypes
from redhawk.codegen.jinja.mapping import ComponentMapper

_projectTypes = {
    ComponentTypes.RESOURCE: 'Component',
    ComponentTypes.DEVICE:   'Device',
    ComponentTypes.LOADABLEDEVICE: 'LoadableDevice',
    ComponentTypes.EXECUTABLEDEVICE: 'ExecutableDevice',
    ComponentTypes.SERVICE:  'Service'
}

class ProjectMapper(ComponentMapper):
    def _mapImplementation(self, impl):
        impldict = {}
        impldict['language'] = impl.programminglanguage()
        # NB: This makes the (reasonable, in practice) assumption that each
        #     implementation is in the same subdirectory as the entry point.
        impldict['outputdir'] = os.path.dirname(impl.entrypoint())
        return impldict

    def _mapComponent(self, softpkg):
        component = {}
        component['type'] = _projectTypes[softpkg.type()]
        component['interfaces'] = [name.lower()+'Interfaces' for name in self.getInterfaceNamespaces(softpkg)]
        return component

    def mapProject(self, softpkg):
        project = self.mapComponent(softpkg)        
        impls = [self.mapImplementation(impl) for impl in softpkg.implementations()]
        project['implementations'] = impls
        project['languages'] = set(impl['language'] for impl in impls)
        project['subdirs'] = [impl['outputdir'] for impl in impls]
        return project
