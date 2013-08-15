import jinja2

from redhawk.codegen.jinja.loader import CodegenLoader
from redhawk.codegen.jinja.common import ShellTemplate, AutomakeTemplate, AutoconfTemplate
from redhawk.codegen.jinja.cpp import CppCodeGenerator, CppTemplate

from mapping import BaseComponentMapper

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

loader = CodegenLoader(__package__,
                       {'common': 'redhawk.codegen.jinja.common'})

class BaseComponentGenerator(CppCodeGenerator):
    def loader(self, component):
        return loader

    def componentMapper(self):
        return BaseComponentMapper()

    def propertyMapper(self):
        return None

    def portMapper(self):
        return None

    def templates(self, component):
        templates = [
            CppTemplate('main.cpp'),
            AutomakeTemplate('Makefile.am'),
            AutomakeTemplate('Makefile.am.ide'),
            AutoconfTemplate('configure.ac'),
            ShellTemplate('build.sh'),
            ShellTemplate('common/reconf')
        ]

        return templates
