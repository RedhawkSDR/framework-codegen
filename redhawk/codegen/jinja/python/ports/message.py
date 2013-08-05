import jinja2

from redhawk.codegen.jinja.ports import PortFactory

from generator import PythonPortGenerator, builtinport

class MessagePortFactory(PortFactory):
    REPID = 'IDL:ExtendedEvent/MessageEvent:1.0'

    def match(self, port):
        return (port.repid() == self.REPID)

    def generator(self, port):
        if port.isProvides():
            return MessageConsumerPortGenerator(port)
        else:
            return MessageSupplierPortGenerator(port)

@builtinport('ossie.events.MessageConsumerPort')
class MessageConsumerPortGenerator(PythonPortGenerator):
    def _ctorArgs(self, name):
        return ('thread_sleep=0.1',)

@builtinport('ossie.events.MessageSupplierPort')
class MessageSupplierPortGenerator(PythonPortGenerator):
    pass
