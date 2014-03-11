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
//% set includeGuard = component.name.upper() + '_IMPL_H'
#ifndef ${includeGuard}
#define ${includeGuard}

#include "${component.baseclass.header}"

class ${className} : public ${baseClass}
{
    ENABLE_LOGGING
    public:
//% if component is not device
        ${className}(const char *uuid, const char *label);
//% else
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl);
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, char *compDev);
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities);
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities, char *compDev);
//% endif
        ~${className}();
        int serviceFunction();
//% if component is device
    protected:
//%     if not component.isafrontendtuner
        void updateUsageState();
//%     endif
/*{%  block callbackMethods %}*/
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
        std::string getTunerType(std::string& allocation_id);
        bool getTunerDeviceControl(std::string& allocation_id);
        std::string getTunerGroupId(std::string& allocation_id);
        std::string getTunerRfFlowId(std::string& allocation_id);
/*{%             set foundInFrontendInterface = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" or
            port.cpptype == "frontend::InAnalogTunerPort" %}*/
/*{%         if foundInAnalogInterface == False %}*/
        double getTunerCenterFrequency(std::string& allocation_id);
        void setTunerCenterFrequency(std::string& allocation_id, double freq);
        double getTunerBandwidth(std::string& allocation_id);
        void setTunerBandwidth(std::string& allocation_id, double bw);
        bool getTunerAgcEnable(std::string& allocation_id);
        void setTunerAgcEnable(std::string& allocation_id, bool enable);
        float getTunerGain(std::string& allocation_id);
        void setTunerGain(std::string& allocation_id, float gain);
        long getTunerReferenceSource(std::string& allocation_id);
        void setTunerReferenceSource(std::string& allocation_id, long source);
        bool getTunerEnable(std::string& allocation_id);
        void setTunerEnable(std::string& allocation_id, bool enable);
/*{%             set foundInAnalogInterface = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InDigitalTunerPort" %}*/
/*{%         if foundInDigitalInterface == False %}*/
        double getTunerOutputSampleRate(std::string& allocation_id);
        void setTunerOutputSampleRate(std::string& allocation_id, double sr);
/*{%             set foundInDigitalInterface = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InGPSPort" %}*/
/*{%         if foundInGPSPort == False %}*/
        frontend::GPSInfo get_gps_info(std::string& port_name);
        void set_gps_info(std::string& port_name, const frontend::GPSInfo &gps_info);
        frontend::GpsTimePos get_gps_time_pos(std::string& port_name);
        void set_gps_time_pos(std::string& port_name, const frontend::GpsTimePos &gps_time_pos);
/*{%             set foundInGPSPort = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InNavDataPort" %}*/
/*{%         if foundInNavDataPort == False %}*/
        frontend::NavigationPacket get_nav_packet(std::string& port_name);
        void set_nav_packet(std::string& port_name, const frontend::NavigationPacket &nav_info);
/*{%             set foundInNavDataPort = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InRFInfoPort" %}*/
/*{%         if foundInRFInfoPort == False %}*/
        std::string get_rf_flow_id(std::string& port_name);
        void set_rf_flow_id(std::string& port_name, const std::string& id);
        frontend::RFInfoPkt get_rfinfo_pkt(std::string& port_name);
        void set_rfinfo_pkt(std::string& port_name, const frontend::RFInfoPkt& pkt);
/*{%             set foundInRFInfoPort = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{%     if port.cpptype == "frontend::InRFSourcePort" %}*/
/*{%         if foundInRFSourcePort == False %}*/
        std::vector<frontend::RFInfoPkt> get_available_rf_inputs(std::string& port_name);
        void set_available_rf_inputs(std::string& port_name, std::vector<frontend::RFInfoPkt> &inputs);
        frontend::RFInfoPkt get_current_rf_input(std::string& port_name);
        void set_current_rf_input(std::string& port_name, const frontend::RFInfoPkt &pkt);
/*{%             set foundInRFSourcePort = True %}*/
/*{%         endif %}*/
/*{%     endif %}*/
/*{% endfor %}*/
/*{% endblock %}*/

    private:
//%     if component.isafrontendtuner
        ////////////////////////////////////////
        // Required device specific functions // -- to be implemented by device developer
        ////////////////////////////////////////

        // these are pure virtual, must be implemented here
        bool _dev_enable(size_t tuner_id);
        bool _dev_disable(size_t tuner_id);
        bool _dev_set_tuning(std::string &tuner_type, frontend::tuning_request &request, size_t tuner_id);
        bool _dev_del_tuning(size_t tuner_id);
//%     endif
        
    protected:
        void construct();
//% endif
};

#endif
