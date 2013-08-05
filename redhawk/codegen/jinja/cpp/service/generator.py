import jinja2

from redhawk.codegen.jinja.loader import CodegenLoader
from redhawk.codegen.jinja.common import ShellTemplate, AutomakeTemplate, AutoconfTemplate
from redhawk.codegen.jinja.cpp import CppCodeGenerator, CppTemplate

from mapping import ServiceMapper

loader = CodegenLoader(__package__,
                       {'common': 'redhawk.codegen.jinja.common'})

class ServiceGenerator(CppCodeGenerator):
    def loader(self, component):
        return loader

    def componentMapper(self):
        return ServiceMapper()

    def propertyMapper(self):
        return None

    def portMapper(self):
        return None

    def templates(self, component):
        templates = [
            CppTemplate('main.cpp'),
            CppTemplate('service.cpp', component['userclass']['file']),
            CppTemplate('service.h', component['userclass']['header']),
            CppTemplate('service_base.cpp', component['baseclass']['file']),
            CppTemplate('service_base.h', component['baseclass']['header']),
            AutomakeTemplate('Makefile.am'),
            AutomakeTemplate('Makefile.am.ide'),
            AutoconfTemplate('configure.ac'),
            ShellTemplate('build.sh'),
            ShellTemplate('common/reconf')
        ]

        return templates
