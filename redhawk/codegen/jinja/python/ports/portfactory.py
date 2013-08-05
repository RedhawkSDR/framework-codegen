from redhawk.codegen.jinja.ports import PortFactoryList

from generic import GenericPortFactory
from bulkio import BulkioPortFactory
from event import PropertyEventPortGenerator
from message import MessagePortFactory

class PythonPortFactory(PortFactoryList):
    def __init__(self):
        factories = (BulkioPortFactory(), PropertyEventPortGenerator, MessagePortFactory(), GenericPortFactory())
        super(PythonPortFactory,self).__init__(*factories)
