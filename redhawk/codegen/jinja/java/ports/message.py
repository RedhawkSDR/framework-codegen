import jinja2

from redhawk.codegen.lang import java
from redhawk.codegen.jinja.java import JavaTemplate
from redhawk.codegen.jinja.ports import PortFactory

from generator import JavaPortGenerator, BuiltinJavaPort

if not '__package__' in locals():
    # Python 2.4 compatibility
    __package__ = __name__.rsplit('.', 1)[0]

class MessagePortFactory(PortFactory):
    REPID = 'IDL:ExtendedEvent/MessageEvent:1.0'

    def match(cls, port):
        return (port.repid() == cls.REPID)

    def generator(cls, port):
        if port.isProvides():
            return MessageConsumerPortGenerator(port)
        else:
            return MessageSupplierPortGenerator(port)

class MessageConsumerPortGenerator(BuiltinJavaPort):
    def __init__(self, port):
        BuiltinJavaPort.__init__(self, 'org.ossie.events.MessageConsumerPort', port)

    def _ctorArgs(self, name):
        return (java.stringLiteral(name),)

class MessageSupplierPortGenerator(JavaPortGenerator):
    def loader(self):
        return jinja2.PackageLoader(__package__)

    def _implementation(self):
        return JavaTemplate('message.java')

    def _ctorArgs(self, name):
        return (java.stringLiteral(name),)
