from redhawk.codegen.lang import java

from generator import JavaPortGenerator, builtinport

@builtinport('org.ossie.events.PropertyEventSupplier')
class PropertyEventPortGenerator(JavaPortGenerator):
    REPID = 'IDL:omg.org/CosEventChannelAdmin/EventChannel:1.0'
    NAME = 'propEvent'

    @classmethod
    def match(cls, port):
        return (port.repid() == cls.REPID) and (port.name() == cls.NAME)

    def _ctorArgs(self, name):
        return (java.stringLiteral(name),)
