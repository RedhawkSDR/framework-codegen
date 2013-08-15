import jinja2

from redhawk.codegen.lang import cpp
from redhawk.codegen.jinja.cpp import CppTemplate

from generator import CppPortGenerator

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

class MessagePortGenerator(CppPortGenerator):
    REPID = 'IDL:ExtendedEvent/MessageEvent:1.0'

    @classmethod
    def match(cls, port):
        return (port.repid() == cls.REPID)

    @classmethod
    def generator(cls, port):
        if port.isProvides():
            return MessageConsumerPortGenerator(port)
        else:
            return MessageSupplierPortGenerator(port)

    def _ctorArgs(self, name):
        return [cpp.stringLiteral(name)]

class MessageConsumerPortGenerator(MessagePortGenerator):
    def headers(self):
        return ('<ossie/MessageInterface.h>',)

    def className(self):
        return 'MessageConsumerPort'

class MessageSupplierPortGenerator(MessagePortGenerator):

    def headers(self):
        return (['<ossie/MessageInterface.h>'])

    def loader(self):
        return jinja2.PackageLoader(__package__)

    def _declaration(self):
        return CppTemplate('message.h')
