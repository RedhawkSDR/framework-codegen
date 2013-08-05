from redhawk.codegen.lang import python

from generator import PythonPortGenerator, builtinport

@builtinport('ossie.events.PropertyEventSupplier')
class PropertyEventPortGenerator(PythonPortGenerator):
    REPID = 'IDL:omg.org/CosEventChannelAdmin/EventChannel:1.0'
    NAME = 'propEvent'

    @classmethod
    def match(cls, port):
        return (port.repid() == cls.REPID) and (port.name() == cls.NAME)

    def _ctorArgs(self, name):
        return ('self',)
