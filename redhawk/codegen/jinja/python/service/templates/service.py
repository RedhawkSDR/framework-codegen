#% set className = component.userclass.name
#% set interface = component.interface
#% set namespace = component.namespace
#% set imports = component.imports

#!/usr/bin/env python
#
# AUTO-GENERATED
#
# Source: ${component.profile.spd}

import sys, signal, copy, os
import logging

from ossie.cf import CF, CF__POA #@UnusedImport
from ossie.service import start_service
from omniORB import CORBA, URI, PortableServer

from ${imports} import ${namespace}, ${namespace}__POA

class ${className}(${namespace}__POA.${interface}):

    def __init__(self, name="${className}", execparams={}):
        self.name = name
        self._log = logging.getLogger(self.name)
        logging.getLogger().setLevel(logging.DEBUG)

    def terminateService(self):
        pass

#{% for function in component.operations %}
    def ${function.name}(self
#{%- for param in function.params %}
, ${param.name} 
#{%- endfor %}
):
        # TODO
        pass

#{% endfor %}
#{% for attribute in component.attributes %}
    def _get_${attribute.name}(self):
        # TODO
        pass
#{% if not attribute.readonly %}

    def _set_${attribute.name}(self, data):
        # TODO
        pass
#{% endif %}

#{% endfor %}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # If there are arguments, use standard service launch
        # You may change the thread_policy to your preference
        start_service(${className}, thread_policy=PortableServer.SINGLE_THREAD_MODEL)  
    else:
        # Otherwise, assume we are being run manually so print out our IOR
        orb = CORBA.ORB_init(sys.argv)
        o = ${className}()
        print orb.object_to_string(o._this())
        orb.run()

