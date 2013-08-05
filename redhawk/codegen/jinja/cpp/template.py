import redhawk.codegen.lang.cpp

from redhawk.codegen.jinja.template import TemplateFile

class CppTemplate(TemplateFile):
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
        return {
            'cpp': redhawk.codegen.lang.cpp
        }
