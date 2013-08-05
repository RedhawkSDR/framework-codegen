#% set className = portgen.className()
class ${className}(${component.baseclass.name}.${portgen.templateClass()}):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.outConnections = {}
        self.port_lock = threading.Lock()

    def connectPort(self, connection, connectionId):
        self.port_lock.acquire()
        try:
            port = connection._narrow(${portgen.corbaClass()})
            self.outConnections[str(connectionId)] = port
        finally:
            self.port_lock.release()

    def disconnectPort(self, connectionId):
        self.port_lock.acquire()
        try:
            self.outConnections.pop(str(connectionId), None)
        finally:
            self.port_lock.release()
#{% for operation in portgen.operations() %}

#{% set arglist = ['self'] + operation.args %}
    def ${operation.name}(${arglist|join(', ')}):
#{% if operation.returns|length > 1 %}
        retVal = []
#{% elif operation.returns|first == 'string' %}
        retVal = ""
#{% elif operation.returns %}
        retVal = None
#{% endif %}
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        ${"retVal = " if operation.returns}port.${operation.name}(${operation.args|join(', ')})
                    except Exception:
                        self.parent._log.exception("The call to ${operation.name} failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()
#{% if operation.returns %}

        return retVal
#{% endif %}
#{% endfor %}
