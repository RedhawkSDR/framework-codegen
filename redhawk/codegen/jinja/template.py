import os

class TemplateFile(object):
    def __init__(self, template, filename=None, executable=False, userfile=False):
        self.template = template
        if filename:
            self.filename = filename
        else:
            self.filename = os.path.basename(self.template)
        self.executable = executable
        self.userfile = userfile

    def options(self):
        return {}

    def filters(self):
        return {}

    def context(self):
        return {}
