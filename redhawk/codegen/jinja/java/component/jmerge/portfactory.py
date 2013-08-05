from redhawk.codegen.jinja.ports import PortFactoryList
from redhawk.codegen.jinja.java.ports.generic import GenericPortFactory
from redhawk.codegen.jinja.java.ports.bulkio import BulkioPortFactory
from redhawk.codegen.jinja.java.ports.event import PropertyEventPortGenerator
from redhawk.codegen.jinja.java.ports.message import MessagePortGenerator

class PullPortFactory(PortFactoryList):
    def __init__(self):
        factories = (BulkioPortFactory(), PropertyEventPortGenerator, MessagePortGenerator, GenericPortFactory())
        super(PullPortFactory,self).__init__(*factories)
