/*#
 * This file is protected by Copyright. Please refer to the COPYRIGHT file 
 * distributed with this source distribution.
 * 
 * This file is part of REDHAWK core.
 * 
 * REDHAWK core is free software: you can redistribute it and/or modify it 
 * under the terms of the GNU Lesser General Public License as published by the 
 * Free Software Foundation, either version 3 of the License, or (at your 
 * option) any later version.
 * 
 * REDHAWK core is distributed in the hope that it will be useful, but WITHOUT 
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License 
 * for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License 
 * along with this program.  If not, see http://www.gnu.org/licenses/.
 #*/
//% set baseClass = component.superclasses[0].name
//% set artifactType = component.artifacttype
//% set className = component.baseclass.name
/*{% block license %}*/
/*# Allow child templates to include license #*/
/*{% endblock %}*/

/*{% block includes %}*/
#include "${component.baseclass.header}"
/*{% endblock %}*/
/*{% block includeExtentions %}*/
/*# Allow for child template extensions #*/
/*{% endblock %}*/

/*{% block headerComment %}*/
/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

    The following class functions are for the base class for the ${artifactType} class. To
    customize any of these functions, do not modify them here. Instead, overload them
    on the child class

******************************************************************************************/
/*{% endblock %}*/

/*{% if component is device %}*/
${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl),
/*{% if component is aggregatedevice %}*/
    AggregateDevice_impl(),
/*{% endif %}*/
    serviceThread(0)
{
    construct();
}

${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, char *compDev) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl, compDev),
/*{% if component is aggregatedevice %}*/
    AggregateDevice_impl(),
/*{% endif %}*/
    serviceThread(0)
{
    construct();
}

${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl, capacities),
/*{% if component is aggregatedevice %}*/
    AggregateDevice_impl(),
/*{% endif %}*/
    serviceThread(0)
{
    construct();
}

${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities, char *compDev) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl, capacities, compDev),
/*{% if component is aggregatedevice %}*/
    AggregateDevice_impl(),
/*{% endif %}*/
    serviceThread(0)
{
    construct();
}
/*{% else %}*/
/*{% block componentConstructor %}*/
${className}::${className}(const char *uuid, const char *label) :
    ${baseClass}(uuid, label),
    serviceThread(0)
{
    construct();
}
/*{% endblock %}*/
/*{% endif %}*/

/*{% block construct %}*/
void ${className}::construct()
{
    Resource_impl::_started = false;
    loadProperties();
    serviceThread = 0;
    
    PortableServer::ObjectId_var oid;
/*{% for port in component.ports %}*/
    ${port.cppname} = new ${port.constructor};
    oid = ossie::corba::RootPOA()->activate_object(${port.name});
/*{%   if port.name == 'propEvent' %}*/
/*{%     for property in component.events %}*/
    ${port.cppname}->registerProperty(this->_identifier, this->naming_service_name, this->getPropertyFromId("${property.identifier}"));
/*{%     endfor %}*/
    this->registerPropertyChangePort(${port.cppname});
/*{%   endif %}*/
/*{%   if loop.last %}*/

/*{%   endif %}*/
/*{% endfor %}*/
/*{% for port in component.ports if port is provides %}*/
    registerInPort(${port.cppname});
/*{% endfor %}*/
/*{% for port in component.ports if port is uses %}*/
    registerOutPort(${port.cppname}, ${port.cppname}->_this());
/*{% endfor %}*/
}
/*{% endblock %}*/

/*******************************************************************************************
    Framework-level functions
    These functions are generally called by the framework to perform housekeeping.
*******************************************************************************************/
/*{% block initialize %}*/
void ${className}::initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException)
{
}
/*{% endblock %}*/

/*{% block start %}*/
void ${className}::start() throw (CORBA::SystemException, CF::Resource::StartError)
{
    boost::mutex::scoped_lock lock(serviceThreadLock);
    if (serviceThread == 0) {
/*{% for port in component.ports if port.start %}*/
        ${port.cppname}->${port.start};
/*{% endfor %}*/
        serviceThread = new ProcessThread<${className}>(this, 0.1);
        serviceThread->start();
    }
    
    if (!Resource_impl::started()) {
    	Resource_impl::start();
    }
}
/*{% endblock %}*/

/*{% block stop %}*/
void ${className}::stop() throw (CORBA::SystemException, CF::Resource::StopError)
{
    boost::mutex::scoped_lock lock(serviceThreadLock);
    // release the child thread (if it exists)
    if (serviceThread != 0) {
/*{% for port in component.ports if port.stop %}*/
        ${port.cppname}->${port.stop};
/*{% endfor %}*/
        if (!serviceThread->release(2)) {
            throw CF::Resource::StopError(CF::CF_NOTSET, "Processing thread did not die");
        }
        serviceThread = 0;
    }
    
    if (Resource_impl::started()) {
    	Resource_impl::stop();
    }
}
/*{% endblock %}*/

/*{% block getPort %}*/
/*{% if component.ports %}*/
CORBA::Object_ptr ${className}::getPort(const char* _id) throw (CORBA::SystemException, CF::PortSupplier::UnknownPort)
{

    std::map<std::string, Port_Provides_base_impl *>::iterator p_in = inPorts.find(std::string(_id));
    if (p_in != inPorts.end()) {
/*{% for port in component.ports if port is provides %}*/
        if (!strcmp(_id,"${port.name}")) {
            ${port.cpptype} *ptr = dynamic_cast<${port.cpptype} *>(p_in->second);
            if (ptr) {
                return ptr->_this();
            }
        }
/*{% endfor %}*/
    }

    std::map<std::string, CF::Port_var>::iterator p_out = outPorts_var.find(std::string(_id));
    if (p_out != outPorts_var.end()) {
        return CF::Port::_duplicate(p_out->second);
    }

    throw (CF::PortSupplier::UnknownPort());
}

/*{% endif %}*/
/*{% endblock %}*/
/*{% block releaseObject %}*/
void ${className}::releaseObject() throw (CORBA::SystemException, CF::LifeCycle::ReleaseError)
{
    // This function clears the ${artifactType} running condition so main shuts down everything
    try {
        stop();
    } catch (CF::Resource::StopError& ex) {
        // TODO - this should probably be logged instead of ignored
    }

    // deactivate ports
    releaseInPorts();
    releaseOutPorts();

/*{% for port in component.ports %}*/
    delete(${port.cppname});
/*{% endfor %}*/

    ${baseClass}::releaseObject();
}
/*{% endblock %}*/

/*{% block loadProperties %}*/
/*{% from "properties/properties.cpp" import addproperty, initsequence %}*/
void ${className}::loadProperties()
{
/*{% for prop in component.properties %}*/
//% if prop.cppvalues
    ${initsequence(prop)|indent(4)}
//% endif
    ${addproperty(prop)|indent(4)}

/*{% endfor %}*/
}
/*{% endblock %}*/

/*{% block extensions %}*/
/*# Allow for child class extensions #*/
/*{% endblock %}*/
