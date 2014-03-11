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
//% set className = component.userclass.name
//% set baseClass = component.baseclass.name
//% set artifactType = component.artifacttype
/**************************************************************************

    This is the ${artifactType} code. This file contains the child class where
    custom functionality can be added to the ${artifactType}. Custom
    functionality to the base class can be extended here. Access to
    the ports can also be done from this class

**************************************************************************/

#include "${component.userclass.header}"

PREPARE_LOGGING(${className})

/*{% if component is device %}*/
${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl)
{
    construct();
}

${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, char *compDev) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl, compDev)
{
    construct();
}

${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl, capacities)
{
    construct();
}

${className}::${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities, char *compDev) :
    ${baseClass}(devMgr_ior, id, lbl, sftwrPrfl, capacities, compDev)
{
    construct();
}
/*{% else %}*/
${className}::${className}(const char *uuid, const char *label) :
    ${baseClass}(uuid, label)
{
    construct();
}
/*{% endif %}*/

${className}::~${className}()
{
}

/*{% if component is device and baseClass == Device_impl %}*/
/**************************************************************************

    This is called automatically after allocateCapacity or deallocateCapacity are called.
    Your implementation should determine the current state of the device:

       setUsageState(CF::Device::IDLE);   // not in use
       setUsageState(CF::Device::ACTIVE); // in use, with capacity remaining for allocation
       setUsageState(CF::Device::BUSY);   // in use, with no capacity remaining for allocation

**************************************************************************/
void ${className}::updateUsageState()
{
}
/*{% endif %}*/

/***********************************************************************************************

    Basic functionality:

        The service function is called by the serviceThread object (of type ProcessThread).
        This call happens immediately after the previous call if the return value for
        the previous call was NORMAL.
        If the return value for the previous call was NOOP, then the serviceThread waits
        an amount of time defined in the serviceThread's constructor.
        
    SRI:
        To create a StreamSRI object, use the following code:
                std::string stream_id = "testStream";
                BULKIO::StreamSRI sri = bulkio::sri::create(stream_id);

    Time:
        To create a PrecisionUTCTime object, use the following code:
                BULKIO::PrecisionUTCTime tstamp = bulkio::time::utils::now();

        
    Ports:

        Data is passed to the serviceFunction through the getPacket call (BULKIO only).
        The dataTransfer class is a port-specific class, so each port implementing the
        BULKIO interface will have its own type-specific dataTransfer.

        The argument to the getPacket function is a floating point number that specifies
        the time to wait in seconds. A zero value is non-blocking. A negative value
        is blocking.  Constants have been defined for these values, bulkio::Const::BLOCKING and
        bulkio::Const::NON_BLOCKING.

        Each received dataTransfer is owned by serviceFunction and *MUST* be
        explicitly deallocated.

        To send data using a BULKIO interface, a convenience interface has been added 
        that takes a std::vector as the data input

        NOTE: If you have a BULKIO dataSDDS port, you must manually call 
              "port->updateStats()" to update the port statistics when appropriate.

        Example:
            // this example assumes that the ${artifactType} has two ports:
            //  A provides (input) port of type bulkio::InShortPort called short_in
            //  A uses (output) port of type bulkio::OutFloatPort called float_out
            // The mapping between the port and the class is found
            // in the ${artifactType} base class header file

            bulkio::InShortPort::dataTransfer *tmp = short_in->getPacket(bulkio::Const::BLOCKING);
            if (not tmp) { // No data is available
                return NOOP;
            }

            std::vector<float> outputData;
            outputData.resize(tmp->dataBuffer.size());
            for (unsigned int i=0; i<tmp->dataBuffer.size(); i++) {
                outputData[i] = (float)tmp->dataBuffer[i];
            }

            // NOTE: You must make at least one valid pushSRI call
            if (tmp->sriChanged) {
                float_out->pushSRI(tmp->SRI);
            }
            float_out->pushPacket(outputData, tmp->T, tmp->EOS, tmp->streamID);

            delete tmp; // IMPORTANT: MUST RELEASE THE RECEIVED DATA BLOCK
            return NORMAL;

        If working with complex data (i.e., the "mode" on the SRI is set to
        true), the std::vector passed from/to BulkIO can be typecast to/from
        std::vector< std::complex<dataType> >.  For example, for short data:

            bulkio::InShortPort::dataTransfer *tmp = myInput->getPacket(bulkio::Const::BLOCKING);
            std::vector<std::complex<short> >* intermediate = (std::vector<std::complex<short> >*) &(tmp->dataBuffer);
            // do work here
            std::vector<short>* output = (std::vector<short>*) intermediate;
            myOutput->pushPacket(*output, tmp->T, tmp->EOS, tmp->streamID);

        Interactions with non-BULKIO ports are left up to the ${artifactType} developer's discretion

    Properties:
        
        Properties are accessed directly as member variables. For example, if the
        property name is "baudRate", it may be accessed within member functions as
        "baudRate". Unnamed properties are given a generated name of the form
        "prop_n", where "n" is the ordinal number of the property in the PRF file.
        Property types are mapped to the nearest C++ type, (e.g. "string" becomes
        "std::string"). All generated properties are declared in the base class
        (${baseClass}).
    
        Simple sequence properties are mapped to "std::vector" of the simple type.
        Struct properties, if used, are mapped to C++ structs defined in the
        generated file "struct_props.h". Field names are taken from the name in
        the properties file; if no name is given, a generated name of the form
        "field_n" is used, where "n" is the ordinal number of the field.
        
        Example:
            // This example makes use of the following Properties:
            //  - A float value called scaleValue
            //  - A boolean called scaleInput
              
            if (scaleInput) {
                dataOut[i] = dataIn[i] * scaleValue;
            } else {
                dataOut[i] = dataIn[i];
            }
            
        Callback methods can be associated with a property so that the methods are
        called each time the property value changes.  This is done by calling 
        addPropertyChangeListener(<property name>, this, &${className}::<callback method>)
        in the constructor.

        Callback methods should take two arguments, both const pointers to the value
        type (e.g., "const float *"), and return void.

        Example:
            // This example makes use of the following Properties:
            //  - A float value called scaleValue
            
        //Add to ${component.userclass.file}
        ${className}::${className}(const char *uuid, const char *label) :
            ${baseClass}(uuid, label)
        {
            addPropertyChangeListener("scaleValue", this, &${className}::scaleChanged);
        }

        void ${className}::scaleChanged(const float *oldValue, const float *newValue)
        {
            std::cout << "scaleValue changed from" << *oldValue << " to " << *newValue
                      << std::endl;
        }
            
        //Add to ${component.userclass.header}
        void scaleChanged(const float* oldValue, const float* newValue);
        
        
************************************************************************************************/
int ${className}::serviceFunction()
{
    LOG_DEBUG(${className}, "serviceFunction() example log message");
    
    return NOOP;
}

void ${className}::construct()
{
    ${baseClass}::construct();
    /***********************************************************************************
     this function is invoked in the constructor
    ***********************************************************************************/
}

//% if component.isafrontendtuner
////////////////////////////////////////
//// Required device specific functions // -- implemented by device developer
//////////////////////////////////////////
bool ${className}::_dev_enable(size_t tuner_id){
    #warning _dev_enable(): DEVELOPER MUST IMPLEMENT THIS METHOD  *********
    return BOOL_VALUE_HERE;
}
bool ${className}::_dev_disable(size_t tuner_id){
    #warning _dev_disable(): DEVELOPER MUST IMPLEMENT THIS METHOD  *********
    return BOOL_VALUE_HERE;
}
bool ${className}::_dev_set_tuning(std::string &tuner_type, frontend::tuning_request &request, size_t tuner_id){
    /************************************************************
    modify this->tunerChannels

    This data structure is a vector of tuner_status structures
    that is referenced by the base class to determine whether
    or not tuners are available
    ************************************************************/
    #warning _dev_set_tuning(): Evaluate whether or not a tuner is added  *********
    return BOOL_VALUE_HERE;
}
bool ${className}::_dev_del_tuning(size_t tuner_id) {
    #warning _dev_del_tuning(): Deallocate an allocated tuner  *********
    return BOOL_VALUE_HERE;
}

/*{% for port in component.ports if port is provides %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
port.cpptype == "frontend::InAnalogTunerPort" or
port.cpptype == "frontend::InFrontendTunerPort" %}*/
/*************************************************************
Functions servicing the tuner control port
*************************************************************/
std::string ${className}::getTunerType(std::string& allocation_id) {
    long idx = getTunerMapping(allocation_id);
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    return frontend_tuner_status[idx].tuner_type;
}
bool ${className}::getTunerDeviceControl(std::string& allocation_id) {
    long idx = getTunerMapping(allocation_id);
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    if (this->tunerChannels[idx].control_allocation_id == allocation_id)
        return true;
    return false;
}
std::string ${className}::getTunerGroupId(std::string& allocation_id) {
    long idx = getTunerMapping(allocation_id);
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    return frontend_tuner_status[idx].group_id;
}
std::string ${className}::getTunerRfFlowId(std::string& allocation_id) {
    long idx = getTunerMapping(allocation_id);
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    return frontend_tuner_status[idx].rf_flow_id;
}

/*{%-     endif %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
port.cpptype == "frontend::InAnalogTunerPort" %}*/

void ${className}::setTunerCenterFrequency(std::string& allocation_id, double freq) {
    long idx = getTunerMapping(allocation_id);
    if(allocation_id != tunerChannels[idx].control_allocation_id)
        throw FRONTEND::FrontendException(("ID "+allocation_id+" does not have authorization to modify the tuner").c_str());
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    if (freq<0) throw FRONTEND::BadParameterException();
    // set hardware to new value. Raise an exception if it's not possible
    this->frontend_tuner_status[idx].center_frequency = freq;
}
double ${className}::getTunerCenterFrequency(std::string& allocation_id) {
    long idx = getTunerMapping(allocation_id);
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    return frontend_tuner_status[idx].center_frequency;
}
void ${className}::setTunerBandwidth(std::string& allocation_id, double bw) {
    long idx = getTunerMapping(allocation_id);
    if(allocation_id != tunerChannels[idx].control_allocation_id)
        throw FRONTEND::FrontendException(("ID "+allocation_id+" does not have authorization to modify the tuner").c_str());
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    if (bw<0) throw FRONTEND::BadParameterException();
    // set hardware to new value. Raise an exception if it's not possible
    this->frontend_tuner_status[idx].bandwidth = bw;
}
double ${className}::getTunerBandwidth(std::string& allocation_id) {
    long idx = getTunerMapping(allocation_id);
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    return frontend_tuner_status[idx].bandwidth;
}
void ${className}::setTunerAgcEnable(std::string& allocation_id, bool enable){throw FRONTEND::NotSupportedException("setTunerAgcEnable not supported");}
bool ${className}::getTunerAgcEnable(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerAgcEnable not supported");return false;}
void ${className}::setTunerGain(std::string& allocation_id, float gain){throw FRONTEND::NotSupportedException("setTunerGain not supported");}
float ${className}::getTunerGain(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerGain not supported");return 0.0;}
void ${className}::setTunerReferenceSource(std::string& allocation_id, long source){throw FRONTEND::NotSupportedException("setTunerReferenceSource not supported");}
long ${className}::getTunerReferenceSource(std::string& allocation_id){throw FRONTEND::NotSupportedException("getTunerReferenceSource not supported");return 0;}
void ${className}::setTunerEnable(std::string& allocation_id, bool enable) {
    long idx = getTunerMapping(allocation_id);
    if(allocation_id != tunerChannels[idx].control_allocation_id)
        throw FRONTEND::FrontendException(("ID "+allocation_id+" does not have authorization to modify the tuner").c_str());
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    // set hardware to new value. Raise an exception if it's not possible
    this->frontend_tuner_status[idx].enabled = enable;
}
bool ${className}::getTunerEnable(std::string& allocation_id) {
    long idx = getTunerMapping(allocation_id);
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    return frontend_tuner_status[idx].enabled;
}

/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" %}*/
void ${className}::setTunerOutputSampleRate(std::string& allocation_id, double sr) {
    long idx = getTunerMapping(allocation_id);
    if(allocation_id != tunerChannels[idx].control_allocation_id)
        throw FRONTEND::FrontendException(("ID "+allocation_id+" does not have authorization to modify the tuner").c_str());
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    if (sr<0) throw FRONTEND::BadParameterException();
    // set hardware to new value. Raise an exception if it's not possible
    this->frontend_tuner_status[idx].sample_rate = sr;
}
double ${className}::getTunerOutputSampleRate(std::string& allocation_id){
    long idx = getTunerMapping(allocation_id);
    if (idx < 0) throw FRONTEND::BadParameterException("Invalid allocation id");
    return frontend_tuner_status[idx].sample_rate;
}
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
/*************************************************************
Functions servicing the RFInfo port(s)
- port_name is the port over which the call was received
*************************************************************/
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

//% endif 
