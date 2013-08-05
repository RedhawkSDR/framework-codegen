from redhawk.codegen.jinja.ports import PortFactoryList

from generic import GenericPortFactory
from bulkio import BulkioPortFactory
from event import PropertyEventPortGenerator
from message import MessagePortGenerator

class CppPortFactory(PortFactoryList):
    def __init__(self):
        factories = (BulkioPortFactory(), PropertyEventPortGenerator, MessagePortGenerator, GenericPortFactory())
        super(CppPortFactory,self).__init__(*factories)
