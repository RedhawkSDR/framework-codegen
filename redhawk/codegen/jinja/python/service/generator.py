from redhawk.codegen.jinja.loader import CodegenLoader
from redhawk.codegen.jinja.common import ShellTemplate, AutomakeTemplate, AutoconfTemplate
from redhawk.codegen.jinja.python import PythonCodeGenerator, PythonTemplate
from redhawk.codegen.jinja.python.properties import PythonPropertyMapper
from redhawk.codegen.jinja.python.ports import PythonPortMapper, PythonPortFactory

from mapping import ServiceMapper

loader = CodegenLoader(__package__,
                       {'common': 'redhawk.codegen.jinja.common',
                        'base':   'redhawk.codegen.jinja.python.component.base',
                        'pull':   'redhawk.codegen.jinja.python.component.pull'})

class ServiceGenerator(PythonCodeGenerator):
    def loader(self, service):
        return loader

    def componentMapper(self):
        return ServiceMapper()

    def propertyMapper(self):
        return PythonPropertyMapper()

    def portMapper(self):
        return PythonPortMapper()

    def portFactory(self):
        return PythonPortFactory()

    def templates(self, service):
        templates = [
            PythonTemplate('service.py', service['userclass']['file'], executable=True),
            AutoconfTemplate('pull/configure.ac'),
            AutomakeTemplate('base/Makefile.am'),
            AutomakeTemplate('base/Makefile.am.ide'),
            ShellTemplate('common/reconf')
        ]
        return templates
