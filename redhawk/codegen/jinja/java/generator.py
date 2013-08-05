from redhawk.codegen.jinja.generator import CodeGenerator

class JavaCodeGenerator(CodeGenerator):
    def sourceFiles(self, component):
        for template in self.templates(component):
            if template.filename.endswith('.java'):
                yield template.filename
