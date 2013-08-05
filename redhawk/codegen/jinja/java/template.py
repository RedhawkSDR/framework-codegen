import redhawk.codegen.lang.java

from redhawk.codegen.jinja.template import TemplateFile

class JavaTemplate(TemplateFile):
    def __init__(self, template, filename=None, package=None, context={}):
        super(JavaTemplate,self).__init__(template, filename)
        self.package = package
        self.__context = context

    def options(self):
        return {
            'trim_blocks':           True,
            'line_statement_prefix': '//%',
            'variable_start_string': '${',
            'variable_end_string':   '}',
            'block_start_string':    '/*{%',
            'block_end_string':      '%}*/'
        }

    def context(self):
        context = {
            'java': redhawk.codegen.lang.java,
            'package': self.package
        }
        context.update(self.__context)
        return context
