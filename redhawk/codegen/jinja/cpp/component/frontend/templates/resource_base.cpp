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
}

${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, char *compDev) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl, compDev),
/*{% if component is aggregatedevice %}*/
    AggregateDevice_impl(),
/*{% endif %}*/
    serviceThread(0)
{
}

${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl, capacities),
/*{% if component is aggregatedevice %}*/
    AggregateDevice_impl(),
/*{% endif %}*/
    serviceThread(0)
{
}

${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities, char *compDev) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl, capacities, compDev),
/*{% if component is aggregatedevice %}*/
    AggregateDevice_impl(),
/*{% endif %}*/
    serviceThread(0)
{
}
/*{% else %}*/
/*{% block componentConstructor %}*/
${className}::${className}(const char *uuid, const char *label) :
    ${baseClass}(uuid, label),
    serviceThread(0)
{
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
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
            port.cpptype == "frontend::InAnalogTunerPort" or
            port.cpptype == "frontend::InFrontendTunerPort" or
            port.cpptype == "frontend::InGPSPort" or
            port.cpptype == "frontend::InNavDataPort" or
            port.cpptype == "frontend::InRFInfoPort" or
            port.cpptype == "frontend::InRFSourcePort" %}*/
    ${port.cppname} = new ${port.constructor};
/*{%     else %}*/
    ${port.cppname} = new ${port.constructor};
/*{%     endif %}*/

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
/*{% if component.hasmultioutport %}*/
    this->addPropertyChangeListener("connectionTable",this,&${className}::connectionTable_changed);
/*{% endif %}*/
/*{% for port in component.ports if port is provides %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
            port.cpptype == "frontend::InAnalogTunerPort" or
            port.cpptype == "frontend::InFrontendTunerPort" %}*/
    this->addPropertyChangeListener("FRONTEND::tuner_status",this,&${className}::frontend_tuner_status_changed);
/*{% endif %}*/
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

/*{% if baseClass != "Device_impl" %}*/
    Device_impl::releaseObject();
/*{% else %}*/
    ${baseClass}::releaseObject();
/*{% endif %}*/
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

/*{% for port in component.ports if port is provides %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
            port.cpptype == "frontend::InAnalogTunerPort" or
            port.cpptype == "frontend::InFrontendTunerPort" %}*/
void ${className}::frontend_tuner_status_changed(const std::vector<frontend_tuner_status_struct_struct>* oldValue, const std::vector<frontend_tuner_status_struct_struct>* newValue)
{
    this->tunerChannels.resize(this->frontend_tuner_status.size());
    for (unsigned int i=0; i<newValue->size(); i++) {
        this->tunerChannels[i].frontend_status = &this->frontend_tuner_status[i];
    }
}

CF::Properties* ${className}::getTunerStatus(std::string& id)
{
    CF::Properties* tmpVal = new CF::Properties();
    long tuner_id = getTunerMapping(id);
    if (tuner_id < 0)
        throw FRONTEND::FrontendException(("ERROR: ID: " + std::string(id) + " IS NOT ASSOCIATED WITH ANY TUNER!").c_str());
    CORBA::Any prop;
    prop <<= *(static_cast<frontend_tuner_status_struct_struct*>(tunerChannels[tuner_id].frontend_status));
    prop >>= tmpVal;

    CF::Properties_var tmp = new CF::Properties(*tmpVal);
    return tmp._retn();
}

std::string ${className}::getTunerType(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerType not supported");return std::string("none");}
bool ${className}::getTunerDeviceControl(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerDeviceControl not supported");return false;}
std::string ${className}::getTunerGroupId(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerGroupId not supported");return std::string("none");}
std::string ${className}::getTunerRfFlowId(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerRfFlowId not supported");return std::string("none");}
/*{%-     endif %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
            port.cpptype == "frontend::InAnalogTunerPort" %}*/
    /*#- add FEI AnalogTuner callback functions #*/ 
void ${className}::setTunerCenterFrequency(std::string& allocation_id, double freq){throw FRONTEND::NotSupportedException("setTunerCenterFrequency not supported");}
double ${className}::getTunerCenterFrequency(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerCenterFrequency not supported");return 0.0;}
void ${className}::setTunerBandwidth(std::string& allocation_id, double bw){throw FRONTEND::NotSupportedException("setTunerBandwidth not supported");}
double ${className}::getTunerBandwidth(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerBandwidth not supported");return 0.0;}
void ${className}::setTunerAgcEnable(std::string& allocation_id, bool enable){throw FRONTEND::NotSupportedException("setTunerAgcEnable not supported");}
bool ${className}::getTunerAgcEnable(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerAgcEnable not supported");return false;}
void ${className}::setTunerGain(std::string& allocation_id, float gain){throw FRONTEND::NotSupportedException("setTunerGain not supported");}
float ${className}::getTunerGain(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerGain not supported");return 0.0;}
void ${className}::setTunerReferenceSource(std::string& allocation_id, long source){throw FRONTEND::NotSupportedException("setTunerReferenceSource not supported");}
long ${className}::getTunerReferenceSource(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerReferenceSource not supported");return 0;}
void ${className}::setTunerEnable(std::string& allocation_id, bool enable){throw FRONTEND::NotSupportedException("setTunerEnable not supported");}
bool ${className}::getTunerEnable(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerEnable not supported");return false;}
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" %}*/
    /*#- add FEI DigitalTuner callback functions #*/
void ${className}::setTunerOutputSampleRate(std::string& allocation_id, double sr){throw FRONTEND::NotSupportedException("setTunerOutputSampleRate not supported");}
double ${className}::getTunerOutputSampleRate(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerOutputSampleRate not supported");return 0.0;}
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InGPSPort" %}*/
frontend::GPSInfo ${className}::get_gps_info(std::string& port_name){frontend::GPSInfo tmp;return tmp;};
void ${className}::set_gps_info(std::string& port_name, const frontend::GPSInfo &gps_info){};
frontend::GpsTimePos ${className}::get_gps_time_pos(std::string& port_name){frontend::GpsTimePos tmp;return tmp;};
void ${className}::set_gps_time_pos(std::string& port_name, const frontend::GpsTimePos &gps_time_pos){};
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InNavDataPort" %}*/
frontend::NavigationPacket ${className}::get_nav_packet(std::string& port_name){frontend::NavigationPacket tmp;return tmp;};
void ${className}::set_nav_packet(std::string& port_name, const frontend::NavigationPacket &nav_info){};
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InRFInfoPort" %}*/
std::string ${className}::get_rf_flow_id(std::string& port_name){return std::string("none");}
void ${className}::set_rf_flow_id(std::string& port_name, const std::string& id){}
frontend::RFInfoPkt ${className}::get_rfinfo_pkt(std::string& port_name){frontend::RFInfoPkt tmp;return tmp;}
void ${className}::set_rfinfo_pkt(std::string& port_name, const frontend::RFInfoPkt &pkt){}
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InRFSourcePort" %}*/
std::vector<frontend::RFInfoPkt> ${className}::get_available_rf_inputs(std::string& port_name){std::vector<frontend::RFInfoPkt> tmp; return tmp;}
void ${className}::set_available_rf_inputs(std::string& port_name, std::vector<frontend::RFInfoPkt> &inputs){}
frontend::RFInfoPkt ${className}::get_current_rf_input(std::string& port_name){frontend::RFInfoPkt tmp;return tmp;}
void ${className}::set_current_rf_input(std::string& port_name, const frontend::RFInfoPkt &pkt){}
/*{%     endif %}*/
/*{% endfor %}*/

/*{% if component.hasmultioutport %}*/
void ${className}::connectionTable_changed(const std::vector<connection_descriptor_struct>* oldValue, const std::vector<connection_descriptor_struct>* newValue)
{
/*{% for port in component.ports %}*/
/*{%     if port.cpptype == "bulkio::OutShortPort" or
    port.cpptype == "bulkio::OutFloatPort" or
    port.cpptype == "bulkio::OutDoublePort" or
    port.cpptype == "bulkio::OutCharPort" or
    port.cpptype == "bulkio::OutOctetPort" or
    port.cpptype == "bulkio::OutUShortPort" or
    port.cpptype == "bulkio::OutLongPort" or
    port.cpptype == "bulkio::OutULongPort" or
    port.cpptype == "bulkio::OutLongLongPort" or
    port.cpptype == "bulkio::OutULongLongPort" or
    port.cpptype == "bulkio::OutURLPort" or
    port.cpptype == "bulkio::OutXMLPort" or
    port.cpptype == "bulkio::OutSDDSPort" %}*/
    // Check to see if port "${port.cppname}" is on connectionTable
    for (std::vector<connection_descriptor_struct>::const_iterator prop_itr = newValue->begin(); prop_itr != newValue->end(); prop_itr++) {
        if (prop_itr->port_name == "${port.cppname}") {
            ${port.cppname}->updateConnectionFilter(*newValue);
            break;
        }
    }
/*{%     endif %}*/
/*{% endfor %}*/
}
void ${className}::reconcileAllocationIdStreamId(const std::string allocation_id, const std::string stream_id, const std::string port_name) {
    if (port_name != "") {
        for (std::vector<connection_descriptor_struct>::iterator prop_itr = this->connectionTable.begin(); prop_itr!=this->connectionTable.end(); prop_itr++) {
            if ((*prop_itr).port_name != port_name)
                continue;
            if ((*prop_itr).stream_id != stream_id)
                continue;
            if ((*prop_itr).connection_name != allocation_id)
                continue;
            // all three match. This is a repeat
            return;
        }
        std::vector<connection_descriptor_struct> old_table = this->connectionTable;
        connection_descriptor_struct tmp;
        tmp.connection_name = allocation_id;
        tmp.port_name = port_name;
        tmp.stream_id = stream_id;
        this->connectionTable.push_back(tmp);
        this->connectionTable_changed(&old_table, &this->connectionTable);
        return;
    }
    std::vector<connection_descriptor_struct> old_table = this->connectionTable;
    connection_descriptor_struct tmp;
/*{% for port in component.ports %}*/
/*{%     if port.cpptype == "bulkio::OutShortPort" or
    port.cpptype == "bulkio::OutFloatPort" or
    port.cpptype == "bulkio::OutDoublePort" or
    port.cpptype == "bulkio::OutCharPort" or
    port.cpptype == "bulkio::OutOctetPort" or
    port.cpptype == "bulkio::OutUShortPort" or
    port.cpptype == "bulkio::OutLongPort" or
    port.cpptype == "bulkio::OutULongPort" or
    port.cpptype == "bulkio::OutLongLongPort" or
    port.cpptype == "bulkio::OutULongLongPort" or
    port.cpptype == "bulkio::OutURLPort" or
    port.cpptype == "bulkio::OutXMLPort" or
    port.cpptype == "bulkio::OutSDDSPort" %}*/
    tmp.connection_name = allocation_id;
    tmp.port_name = "${port.cppname}";
    tmp.stream_id = stream_id;
    this->connectionTable.push_back(tmp);
/*{%     endif %}*/
/*{% endfor %}*/
    this->connectionTable_changed(&old_table, &this->connectionTable);
}

void ${className}::removeAllocationIdRouting(const std::string allocation_id) {
    std::vector<connection_descriptor_struct> old_table = this->connectionTable;
    std::vector<connection_descriptor_struct>::iterator itr = this->connectionTable.begin();
    while (itr != this->connectionTable.end()) {
        if ((*itr).connection_name == allocation_id) {
            this->connectionTable.erase(itr);
            continue;
        }
        itr++;
    }
    this->connectionTable_changed(&old_table, &this->connectionTable);
}

void ${className}::removeStreamIdRouting(const std::string stream_id, const std::string allocation_id) {
    std::vector<connection_descriptor_struct> old_table = this->connectionTable;
    std::vector<connection_descriptor_struct>::iterator itr = this->connectionTable.begin();
    while (itr != this->connectionTable.end()) {
        if (allocation_id == "") {
            if ((*itr).stream_id == stream_id) {
                this->connectionTable.erase(itr);
                continue;
            }
        } else {
            if (((*itr).stream_id == stream_id) and ((*itr).connection_name == allocation_id)) {
                this->connectionTable.erase(itr);
                continue;
            }
        }
        itr++;
    }
    this->connectionTable_changed(&old_table, &this->connectionTable);
}
/*{% else %}*/
void ${className}::removeAllocationIdRouting(const std::string allocation_id) {
}
/*{% endif %}*/

/*{% block extensions %}*/
/*# Allow for child class extensions #*/
/*{% endblock %}*/
