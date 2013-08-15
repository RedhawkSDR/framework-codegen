from redhawk.codegen.lang import java

from generator import BuiltinJavaPort

class PropertyEventPortGenerator(BuiltinJavaPort):
    REPID = 'IDL:omg.org/CosEventChannelAdmin/EventChannel:1.0'
    NAME = 'propEvent'

    def __init__(self, port):
        BuiltinJavaPort.__init__(self, 'org.ossie.events.PropertyEventSupplier', port)

    @classmethod
    def match(cls, port):
        return (port.repid() == cls.REPID) and (port.name() == cls.NAME)

    def _ctorArgs(self, name):
        return (java.stringLiteral(name),)
