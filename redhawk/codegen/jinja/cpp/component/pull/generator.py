from redhawk.codegen.jinja.generator import CodeGenerator
from redhawk.codegen.jinja.loader import CodegenLoader
from redhawk.codegen.jinja.common import ShellTemplate, AutomakeTemplate, AutoconfTemplate
from redhawk.codegen.jinja.cpp import CppCodeGenerator, CppTemplate
from redhawk.codegen.jinja.cpp.properties import CppPropertyMapper
from redhawk.codegen.jinja.cpp.ports import CppPortMapper, CppPortFactory

from mapping import PullComponentMapper

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

loader = CodegenLoader(__package__,
                       {'common'     : 'redhawk.codegen.jinja.common',
                        'base'       : 'redhawk.codegen.jinja.cpp.component.base',
                        'properties' : 'redhawk.codegen.jinja.cpp.properties'})

class PullComponentGenerator(CppCodeGenerator):
    # Need to keep use_vector_impl, auto_start and queued_ports to handle legacy options 
    def parseopts (self, use_vector_impl=True,auto_start=True,queued_ports=False):
        pass

    def loader(self, component):
        return loader

    def componentMapper(self):
        return PullComponentMapper()

    def propertyMapper(self):
        return CppPropertyMapper()

    def portMapper(self):
        return CppPortMapper()

    def portFactory(self):
        return CppPortFactory()

    def templates(self, component):
        templates = [
            CppTemplate('resource.cpp', component['userclass']['file'], userfile=True),
            CppTemplate('resource.h', component['userclass']['header'], userfile=True),
            CppTemplate('resource_base.cpp', component['baseclass']['file']),
            CppTemplate('resource_base.h', component['baseclass']['header']),
            CppTemplate('base/main.cpp'),
            AutomakeTemplate('base/Makefile.am'),
            AutomakeTemplate('base/Makefile.am.ide'),
            AutoconfTemplate('base/configure.ac'),
            ShellTemplate('base/build.sh'),
            ShellTemplate('common/reconf')
        ]

        for gen in component['portgenerators']:
            # Need to include port_impl if a non-bulkio port exists
            if str(type(gen)).find("BulkioPortGenerator") == -1:
                templates.append(CppTemplate('port_impl.cpp'))
                templates.append(CppTemplate('port_impl.h'))
                break

        if component['structdefs']:
            templates.append(CppTemplate('struct_props.h'))

        return templates
