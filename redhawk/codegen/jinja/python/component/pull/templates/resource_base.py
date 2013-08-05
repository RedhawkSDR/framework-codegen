#% set className = component.baseclass.name
#% set superclass = component.superclass.name
#% set artifactType = component.superclass.artifactType
#!/usr/bin/env python
#
# AUTO-GENERATED CODE.  DO NOT MODIFY!
#
# Source: ${component.profile.spd}
from ossie.cf import CF, CF__POA
from ossie.utils import uuid

#{% if component is device %}
from ossie.device import ${superclass}
#{% else %}
from ossie.resource import Resource
#{% endif %}
#{% if component.properties|test('simple') is sometimes(true) or component.structdefs %}
from ossie.properties import simple_property
#{% endif %}
#{% if component.properties|test('simplesequence') is sometimes(true) %}
from ossie.properties import simpleseq_property
#{% endif %}
#{% if component.structdefs %}
from ossie.properties import struct_property
#{% endif %}
#{% if component.properties|test('structsequence') is sometimes(true) %}
from ossie.properties import structseq_property
#{% endif %}

import Queue, copy, time, threading
#{% filter lines|unique|join('\n') %}
#{% for portgen in component.portgenerators %}
#{%   if loop.first %}
from ossie.resource import usesport, providesport
#{%     if component.hasbulkio %}
import bulkio
#{%     endif %}
#{%   endif %}
#{%   for statement in portgen.imports() %}
${statement}
#{%   endfor %}
#{% endfor %}
#{% endfilter %}

NOOP = -1
NORMAL = 0
FINISH = 1
class ProcessThread(threading.Thread):
    def __init__(self, target, pause=0.0125):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.target = target
        self.pause = pause
        self.stop_signal = threading.Event()

    def stop(self):
        self.stop_signal.set()

    def updatePause(self, pause):
        self.pause = pause

    def run(self):
        state = NORMAL
        while (state != FINISH) and (not self.stop_signal.isSet()):
            state = self.target()
            if (state == NOOP):
                # If there was no data to process sleep to avoid spinning
                time.sleep(self.pause)

class ${className}(${component.poaclass}, ${superclass}):
        # These values can be altered in the __init__ of your derived class

        PAUSE = 0.0125 # The amount of time to sleep if process return NOOP
        TIMEOUT = 5.0 # The amount of time to wait for the process thread to die when stop() is called
        DEFAULT_QUEUE_SIZE = 100 # The number of BulkIO packets that can be in the queue before pushPacket will block

#{% if component is device %}
        def __init__(self, devmgr, uuid, label, softwareProfile, compositeDevice, execparams):
            ${superclass}.__init__(self, devmgr, uuid, label, softwareProfile, compositeDevice, execparams)
#{% else %}
        def __init__(self, identifier, execparams):
            loggerName = (execparams['NAME_BINDING'].replace('/', '.')).rsplit("_", 1)[0]
            Resource.__init__(self, identifier, execparams, loggerName=loggerName)
#{% endif %}
            self.threadControlLock = threading.RLock()
            self.process_thread = None
            # self.auto_start is deprecated and is only kept for API compatability
            # with 1.7.X and 1.8.0 ${artifactType}s.  This variable may be removed
            # in future releases
            self.auto_start = False

        def initialize(self):
            ${superclass}.initialize(self)
            
            # Instantiate the default implementations for all ports on this ${artifactType}
#{% for port in component.ports %}
            self.${port.pyname} = ${port.constructor}
#{% endfor %}

        def start(self):
            self.threadControlLock.acquire()
            try:
                ${superclass}.start(self)
                if self.process_thread == None:
                    self.process_thread = ProcessThread(target=self.process, pause=self.PAUSE)
                    self.process_thread.start()
            finally:
                self.threadControlLock.release()

        def process(self):
            """The process method should process a single "chunk" of data and then return.  This method will be called
            from the processing thread again, and again, and again until it returns FINISH or stop() is called on the
            ${artifactType}.  If no work is performed, then return NOOP"""
            raise NotImplementedError

        def stop(self):
            self.threadControlLock.acquire()
            try:
                process_thread = self.process_thread
                self.process_thread = None

                if process_thread != None:
                    process_thread.stop()
                    process_thread.join(self.TIMEOUT)
                    if process_thread.isAlive():
                        raise CF.Resource.StopError(CF.CF_NOTSET, "Processing thread did not die")
                ${superclass}.stop(self)
            finally:
                self.threadControlLock.release()

        def releaseObject(self):
            try:
                self.stop()
            except Exception:
                self._log.exception("Error stopping")
            self.threadControlLock.acquire()
            try:
                ${superclass}.releaseObject(self)
            finally:
                self.threadControlLock.release()

        ######################################################################
        # PORTS
        # 
        # DO NOT ADD NEW PORTS HERE.  You can add ports in your derived class, in the SCD xml file, 
        # or via the IDE.

#{% for portgen in component.portgenerators if portgen.hasImplementation() %}
        # '${portgen.namespace}/${portgen.interface}' port
        class ${portgen.templateClass()}(${portgen.poaClass()}):
            """This class is a port template for the ${portgen.className()} port and
            should not be instantiated nor modified.
            
            The expectation is that the specific port implementation will extend
            from this class instead of the base CORBA class ${portgen.poaClass()}.
            """
            pass

#{% endfor %}
#{% for port in component.ports %}
#{%   filter codealign %}
        ${port.pyname} = ${port.generator.direction}port(name="${port.name}",
                                                         repid="${port.repid}",
                                                         type_="${port.types[0]}")
#{%   endfilter %}

#{% endfor %}
        ######################################################################
        # PROPERTIES
        # 
        # DO NOT ADD NEW PROPERTIES HERE.  You can add properties in your derived class, in the PRF xml file
        # or by using the IDE.
#{% import "base/properties.py" as properties with context %}
#{% for prop in component.properties if prop is simple %}
        ${properties.simple(prop)|indent(8)}
#{% endfor %}
#{% for prop in component.properties if prop is simplesequence %}
        ${properties.simplesequence(prop)|indent(8)}
#{% endfor %}
#{% for prop in component.properties if prop is struct %}
        ${properties.structdef(prop)|indent(8)}

        ${properties.struct(prop)|indent(8)}
#{% endfor %}
#{% for prop in component.properties if prop is structsequence %}
        ${properties.structdef(prop.structdef,False)|indent(8)}

        ${properties.structsequence(prop)|indent(8)}
#{% endfor %}
#{% for portgen in component.portgenerators if portgen is provides and portgen.hasImplementation() %}

#{%   if loop.first %}
'''provides port(s)'''

#{%   endif %}
#{% include portgen.implementation() %}
#{% endfor %}
#{% for portgen in component.portgenerators if portgen is uses and portgen.hasImplementation() %}

#{%   if loop.first %}
'''uses port(s)'''

#{%   endif %}
#{% include portgen.implementation() %}
#{% endfor %}
