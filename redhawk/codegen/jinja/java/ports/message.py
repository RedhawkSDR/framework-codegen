import jinja2

from redhawk.codegen.lang import java
from redhawk.codegen.jinja.java import JavaTemplate

from generator import JavaPortGenerator, builtinport

class MessagePortGenerator(JavaPortGenerator):
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
        return (java.stringLiteral(name),)

@builtinport('org.ossie.events.MessageConsumerPort')
class MessageConsumerPortGenerator(MessagePortGenerator):
    pass

class MessageSupplierPortGenerator(MessagePortGenerator):
    def loader(self):
        return jinja2.PackageLoader(__package__)

    def _implementation(self):
        return JavaTemplate('message.java')
