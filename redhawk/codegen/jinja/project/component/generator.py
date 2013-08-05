import jinja2

from redhawk.codegen.jinja.generator import TopLevelGenerator
from redhawk.codegen.jinja.mapping import ComponentMapper
from redhawk.codegen.jinja.common import ShellTemplate, SpecfileTemplate

from mapping import ProjectMapper

loader = jinja2.PackageLoader(__package__)

class ComponentProjectGenerator(TopLevelGenerator):
    def projectMapper(self):
        return ProjectMapper()

    def loader(self, project):
        return loader

    def templates(self, project):
        return [
            ShellTemplate('build.sh'),
            SpecfileTemplate('component.spec', project['name']+'.spec')
            ]
