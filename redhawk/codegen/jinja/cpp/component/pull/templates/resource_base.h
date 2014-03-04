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
#include ${superclass.header}
/*{% endfor %}*/
/*{% block includeExtentions %}*/
/*# Allow for child template extensions #*/
/*{% endblock %}*/

/*{% filter lines|unique|join('\n') %}*/
/*{%   for portgen in component.portgenerators if portgen.header() %}*/
#include ${portgen.header()}
/*{%   endfor %}*/
/*{% endfilter %}*/
/*{% if "struct_props.h" in generator.sourceFiles(component) %}*/
#include "struct_props.h"
/*{% endif %}*/
/*{% endblock %}*/

/*{% block defines %}*/
#define NOOP 0
#define FINISH -1
#define NORMAL 1
/*{% endblock %}*/

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
        void connectionTable_changed(const std::vector<connection_descriptor_struct>* oldValue, const std::vector<connection_descriptor_struct>* newValue);
/*{% endif %}*/

    protected:
/*{% block baseProtectedMembers %}*/
        ProcessThread<${className}> *serviceThread; 
        boost::mutex serviceThreadLock;
/*{% for prop in component.properties %}*/
/*{%   if loop.first %}*/

        // Member variables exposed as properties
/*{%   endif %}*/
        ${prop.cpptype} ${prop.cppname};
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

    private:
        void construct();

/*{% block extendedPrivate%}*/
/*{% endblock %}*/

/*{% block extensions %}*/
/*# Allow for child template extensions #*/
/*{% endblock %}*/
};
#endif
