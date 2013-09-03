from redhawk.codegen.jinja.loader import CodegenLoader
from redhawk.codegen.jinja.common import ShellTemplate, AutomakeTemplate, AutoconfTemplate
from redhawk.codegen.jinja.python import PythonCodeGenerator, PythonTemplate
from redhawk.codegen.jinja.python.properties import PythonPropertyMapper
from redhawk.codegen.jinja.python.ports import PythonPortMapper, PythonPortFactory

from mapping import PullComponentMapper

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

loader = CodegenLoader(__package__,
                       {'common': 'redhawk.codegen.jinja.common',
                        'base':   'redhawk.codegen.jinja.python.component.base'})

class PullComponentGenerator(PythonCodeGenerator):
    # Need to keep auto_start and queued_ports to handle legacy options
    def parseopts (self, auto_start=True,queued_ports=False):
        pass

    def loader(self, component):
        return loader

    def componentMapper(self):
        return PullComponentMapper()

    def propertyMapper(self):
        return PythonPropertyMapper()

    def portMapper(self):
        return PythonPortMapper()

    def portFactory(self):
        return PythonPortFactory()

    def templates(self, component):
        templates = [
            PythonTemplate('resource_base.py', component['baseclass']['file']),
            PythonTemplate('resource.py', component['userclass']['file'], executable=True, userfile=True),
            AutoconfTemplate('configure.ac'),
            AutomakeTemplate('base/Makefile.am'),
            AutomakeTemplate('base/Makefile.am.ide'),
            ShellTemplate('common/reconf')
        ]
        return templates
