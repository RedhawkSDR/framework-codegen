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
//% set includeGuard = component.name.upper() + '_IMPL_BASE_H'
//% set className = component.baseclass.name
/*{% block license %}*/
/*# Allow child templates to include license #*/
/*{% endblock %}*/

/*{% block includeGuard %}*/
#ifndef ${includeGuard}
#define ${includeGuard}
/*{% endblock %}*/

/*{% block includes %}*/
#include <boost/thread.hpp>
/*{% for superclass in component.superclasses %}*/
/*{%     if superclass.header != '' %}*/
#include ${superclass.header}
/*{%     endif %}*/
/*{% endfor %}*/
/*{% block includeExtentions %}*/
/*# Allow for child template extensions #*/
/*{% endblock %}*/

/*{% if component.hasbulkio %}*/
#include <bulkio/bulkio.h>
/*{% endif %}*/
/*{% if "port_impl.h" in generator.sourceFiles(component) %}*/
#include "port_impl.h"
/*{% endif %}*/
/*{% if "struct_props.h" in generator.sourceFiles(component) %}*/
#include "struct_props.h"
/*{% endif %}*/
/*{% endblock %}*/

/*{% block defines %}*/
#define NOOP 0
#define FINISH -1
#define NORMAL 1
/*{% endblock %}*/

#define BOOL_VALUE_HERE 0
#define DOUBLE_VALUE_HERE 0

class ${className};

/*{% block processThread %}*/
template < typename TargetClass >
class ProcessThread
{
    public:
/*{% block processThreadConstructor %}*/
        ProcessThread(TargetClass *_target, float _delay) :
            target(_target)
        {
            _mythread = 0;
            _thread_running = false;
            _udelay = (__useconds_t)(_delay * 1000000);
        };
/*{% endblock %}*/

/*{% block processThreadStart %}*/
        // kick off the thread
        void start() {
            if (_mythread == 0) {
                _thread_running = true;
                _mythread = new boost::thread(&ProcessThread::run, this);
            }
        };
/*{% endblock %}*/

/*{% block processThreadRun %}*/
        // manage calls to target's service function
        void run() {
            int state = NORMAL;
            while (_thread_running and (state != FINISH)) {
                state = target->serviceFunction();
                if (state == NOOP) usleep(_udelay);
            }
        };
/*{% endblock %}*/

/*{% block processThreadRelease %}*/
        // stop thread and wait for termination
        bool release(unsigned long secs = 0, unsigned long usecs = 0) {
            _thread_running = false;
            if (_mythread)  {
                if ((secs == 0) and (usecs == 0)){
                    _mythread->join();
                } else {
                    boost::system_time waitime= boost::get_system_time() + boost::posix_time::seconds(secs) +  boost::posix_time::microseconds(usecs) ;
                    if (!_mythread->timed_join(waitime)) {
                        return 0;
                    }
                }
                delete _mythread;
                _mythread = 0;
            }
    
            return 1;
        };
/*{% endblock %}*/

/*{% block processThreadDestructor %}*/
        virtual ~ProcessThread(){
            if (_mythread != 0) {
                release(0);
                _mythread = 0;
            }
        };
/*{% endblock %}*/

/*{% block processThreadUpdateDelay %}*/
        void updateDelay(float _delay) { _udelay = (__useconds_t)(_delay * 1000000); };
/*{% endblock %}*/

/*{% block publicProcessThreadExtensions %}*/
/*# Allow for child templates to extend this class #*/
/*{% endblock %}*/

    private:
/*{% block processThreadPrivateVars %}*/
        boost::thread *_mythread;
        bool _thread_running;
        TargetClass *target;
        __useconds_t _udelay;
        boost::condition_variable _end_of_run;
        boost::mutex _eor_mutex;
/*{% endblock %}*/
};
/*{% endblock %}*/

/*{% block classPrototype %}*/
class ${className} : public ${component.superclasses|join(', public ', attribute='name')}
/*{% endblock %}*/
{
/*{% for portgen in component.portgenerators if portgen.hasDeclaration() %}*/
    friend class ${portgen.className()};
/*{%   if loop.last %}*/

/*{%   endif %}*/
/*{% endfor %}*/
    public:
/*{% block baseConstructor %}*/
/*{% if component is device %}*/
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl);
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, char *compDev);
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities);
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities, char *compDev);
/*{% else %}*/
        ${className}(const char *uuid, const char *label);
/*{% endif %}*/
/*{% endblock %}*/

/*{% block cfResource %}*/
        void start() throw (CF::Resource::StartError, CORBA::SystemException);

        void stop() throw (CF::Resource::StopError, CORBA::SystemException);

/*{% if component.ports %}*/
        CORBA::Object_ptr getPort(const char* _id) throw (CF::PortSupplier::UnknownPort, CORBA::SystemException);

/*{% endif %}*/
        void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

        void initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException);
/*{% endblock %}*/

/*{% block basePublicFunctions %}*/
        void loadProperties();

        virtual int serviceFunction() = 0;
/*{% endblock %}*/

/*{% if component.hasmultioutport %}*/
        void connectionTableChanged(const std::vector<connection_descriptor_struct>* oldValue, const std::vector<connection_descriptor_struct>* newValue);
        void matchAllocationIdToStreamId(const std::string allocation_id, const std::string stream_id, const std::string port_name="");
        void removeAllocationIdRouting(const size_t tuner_id);
        void removeStreamIdRouting(const std::string stream_id, const std::string allocation_id="");
/*{% else %}*/
        void removeAllocationIdRouting(const size_t tuner_id);
/*{% endif %}*/

/*{% block callbackMethods %}*/
/*{% set foundInFrontendInterface = False %}*/
/*{% set foundInAnalogInterface = False %}*/
/*{% set foundInDigitalInterface = False %}*/
/*{% set foundInGPSPort = False %}*/
/*{% set foundInNavDataPort = False %}*/
/*{% set foundInRFInfoPort = False %}*/
/*{% set foundInRFSourcePort = False %}*/
/*{% for port in component.ports if port is provides %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
            port.cpptype == "frontend::InAnalogTunerPort" or
            port.cpptype == "frontend::InFrontendTunerPort" %}*/
/*{%         if foundInFrontendInterface == False %}*/ 
        virtual std::string getTunerType(std::string& allocation_id);
        virtual bool getTunerDeviceControl(std::string& allocation_id);
        virtual std::string getTunerGroupId(std::string& allocation_id);
        virtual std::string getTunerRfFlowId(std::string& allocation_id);
        virtual CF::Properties* getTunerStatus(std::string& allocation_id);
        virtual void assignListener(std::string& listen_alloc_id, std::string& allocation_id);
        virtual void removeListener(std::string& listen_alloc_id);
/*{%             set foundInFrontendInterface = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
            port.cpptype == "frontend::InAnalogTunerPort" %}*/
/*{%         if foundInAnalogInterface == False %}*/ 
        virtual double getTunerCenterFrequency(std::string& allocation_id);
        virtual void setTunerCenterFrequency(std::string& allocation_id, double freq);
        virtual double getTunerBandwidth(std::string& allocation_id);
        virtual void setTunerBandwidth(std::string& allocation_id, double bw);
        virtual bool getTunerAgcEnable(std::string& allocation_id);
        virtual void setTunerAgcEnable(std::string& allocation_id, bool enable);
        virtual float getTunerGain(std::string& allocation_id);
        virtual void setTunerGain(std::string& allocation_id, float gain);
        virtual long getTunerReferenceSource(std::string& allocation_id);
        virtual void setTunerReferenceSource(std::string& allocation_id, long source);
        virtual bool getTunerEnable(std::string& allocation_id);
        virtual void setTunerEnable(std::string& allocation_id, bool enable);
/*{%             set foundInAnalogInterface = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" %}*/
/*{%         if foundInDigitalInterface == False %}*/ 
        virtual double getTunerOutputSampleRate(std::string& allocation_id);
        virtual void setTunerOutputSampleRate(std::string& allocation_id,double sr);
/*{%             set foundInDigitalInterface = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InGPSPort" %}*/
/*{%         if foundInGPSPort == False %}*/ 
        virtual frontend::GPSInfo get_gps_info(std::string& port_name);
        virtual void set_gps_info(std::string& port_name, const frontend::GPSInfo &gps_info);
        virtual frontend::GpsTimePos get_gps_time_pos(std::string& port_name);
        virtual void set_gps_time_pos(std::string& port_name, const frontend::GpsTimePos &gps_time_pos);
/*{%             set foundInGPSPort = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InNavDataPort" %}*/
/*{%         if foundInNavDataPort == False %}*/ 
        virtual frontend::NavigationPacket get_nav_packet(std::string& port_name);
        virtual void set_nav_packet(std::string& port_name, const frontend::NavigationPacket &nav_info);
/*{%             set foundInNavDataPort = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InRFInfoPort" %}*/
/*{%         if foundInRFInfoPort == False %}*/ 
        virtual std::string get_rf_flow_id(std::string& port_name);
        virtual void set_rf_flow_id(std::string& port_name, const std::string& id);
        virtual frontend::RFInfoPkt get_rfinfo_pkt(std::string& port_name);
        virtual void set_rfinfo_pkt(std::string& port_name, const frontend::RFInfoPkt& pkt);
/*{%             set foundInRFInfoPort = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InRFSourcePort" %}*/
/*{%         if foundInRFSourcePort == False %}*/ 
        virtual std::vector<frontend::RFInfoPkt> get_available_rf_inputs(std::string& port_name);
        virtual void set_available_rf_inputs(std::string& port_name, std::vector<frontend::RFInfoPkt> &inputs);
        virtual frontend::RFInfoPkt get_current_rf_input(std::string& port_name);
        virtual void set_current_rf_input(std::string& port_name, const frontend::RFInfoPkt &pkt);
/*{%             set foundInRFSourcePort = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{% endfor %}*/
/*{% endblock %}*/
/*{% for port in component.ports if port is provides %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
         port.cpptype == "frontend::InAnalogTunerPort" or
         port.cpptype == "frontend::InFrontendTunerPort" %}*/
        void frontendTunerStatusChanged(const std::vector<frontend_tuner_status_struct_struct>* oldValue, const std::vector<frontend_tuner_status_struct_struct>* newValue);
/*{%     endif %}*/
/*{% endfor %}*/
        
    protected:
/*{% block baseProtectedMembers %}*/
        ProcessThread<${className}> *serviceThread; 
        boost::mutex serviceThreadLock;
/*{% for port in component.ports if port is provides %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
            port.cpptype == "frontend::InAnalogTunerPort" or
            port.cpptype == "frontend::InFrontendTunerPort" %}*/
        std::map<std::string, std::string> listeners;
/*{%     endif %}*/
/*{% endfor %}*/
/*{% for prop in component.properties %}*/
/*{%   if loop.first %}*/

        // Member variables exposed as properties
/*{%   endif %}*/
/*{%   if ((not component.isafrontendtuner) or
           (component.isafrontendtuner and
            prop.cppname != "device_kind" and
            prop.cppname != "device_model" and
            prop.cppname != "frontend_tuner_status" and
            prop.cppname != "frontend_tuner_allocation" and
            prop.cppname != "frontend_listener_allocation")) %}*/
        ${prop.cpptype} ${prop.cppname};
/*{%   endif %}*/
/*{% endfor %}*/
/*{% for port in component.ports %}*/
/*{%   if loop.first %}*/

        // Ports
/*{%   endif %}*/
        ${port.cpptype} *${port.cppname};
/*{% endfor %}*/
/*{% endblock %}*/

/*{% block extendedProtected%}*/
/*{% endblock %}*/
        virtual void setNumChannels(size_t num);
        void construct();

/*{% block extensions %}*/
/*# Allow for child template extensions #*/
/*{% endblock %}*/
};
#endif
