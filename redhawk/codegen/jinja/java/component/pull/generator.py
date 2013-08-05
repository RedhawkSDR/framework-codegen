import os

from redhawk.codegen import utils

from redhawk.codegen.jinja.loader import CodegenLoader
from redhawk.codegen.jinja.common import ShellTemplate, AutomakeTemplate, AutoconfTemplate
from redhawk.codegen.jinja.java import JavaCodeGenerator, JavaTemplate
from redhawk.codegen.jinja.java.properties import JavaPropertyMapper
from redhawk.codegen.jinja.java.ports import JavaPortMapper

from mapping import PullComponentMapper
from portfactory import PullPortFactory

loader = CodegenLoader(__package__,
                       {'base': 'redhawk.codegen.jinja.java.component.base',
                        'common': 'redhawk.codegen.jinja.common'})

class PullComponentGenerator(JavaCodeGenerator):
    # Need to keep use_jni and auto_start to handle legacy options
    def parseopts (self, java_package='',use_jni=True, auto_start=True):
        self.package = java_package

    def loader(self, component):
        return loader

    def componentMapper(self):
        return PullComponentMapper(self.package)

    def propertyMapper(self):
        return JavaPropertyMapper()

    def portMapper(self):
        return JavaPortMapper()

    def portFactory(self):
        return PullPortFactory()

    def templates(self, component):
        # Put generated Java files in "src" subdirectory, followed by their
        # package path.
        pkgpath = os.path.join('src', *component['package'].split('.'))
        userfile = component['userclass']['file']
        basefile = component['baseclass']['file']
        templates = [
            JavaTemplate('resource.java', os.path.join(pkgpath, userfile)),
            JavaTemplate('resource_base.java', os.path.join(pkgpath, basefile)),
            AutomakeTemplate('base/Makefile.am'),
            AutoconfTemplate('base/configure.ac'),
            ShellTemplate('base/startJava.sh'),
            ShellTemplate('common/reconf')
        ]

        portpkg = component['package'] + '.' + 'ports'
        portpkgpath = os.path.join(pkgpath, 'ports')
        for generator in component['portgenerators']:
            if not generator.hasImplementation():
                continue
            generator.package = portpkg
            template = generator.implementation()
            filename = os.path.join(portpkgpath, generator.className()+'.java')
            context = {'portgenerator': generator}
            templates.append(JavaTemplate(template, filename, portpkg, context))

        return templates
