import os

class TemplateFile(object):
    def __init__(self, template, filename=None, executable=False):
        self.template = template
        if filename:
            self.filename = filename
        else:
            self.filename = os.path.basename(self.template)
        self.executable = executable

    def options(self):
        return {}

    def filters(self):
        return {}

    def context(self):
        return {}
