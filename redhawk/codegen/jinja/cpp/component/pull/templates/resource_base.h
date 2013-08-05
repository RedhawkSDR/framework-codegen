//% set includeGuard = component.name.upper() + '_IMPL_BASE_H'
//% set className = component.baseclass.name
//% set superclass = component.superclass.name
#ifndef ${includeGuard}
#define ${includeGuard}

#include <boost/thread.hpp>
#include ${component.superclass.header}

/*{% if component.hasbulkio %}*/
#include "bulkio/bulkio.h"
/*{% endif %}*/
/*{% if "port_impl.h" in generator.sourceFiles(component) %}*/
#include "port_impl.h"
/*{% endif %}*/
/*{% if "struct_props.h" in generator.sourceFiles(component) %}*/
#include "struct_props.h"
/*{% endif %}*/

#define NOOP 0
#define FINISH -1
#define NORMAL 1

class ${className};

template < typename TargetClass >
class ProcessThread
{
    public:
        ProcessThread(TargetClass *_target, float _delay) :
            target(_target)
        {
            _mythread = 0;
            _thread_running = false;
            _udelay = (__useconds_t)(_delay * 1000000);
        };

        // kick off the thread
        void start() {
            if (_mythread == 0) {
                _thread_running = true;
                _mythread = new boost::thread(&ProcessThread::run, this);
            }
        };

        // manage calls to target's service function
        void run() {
            int state = NORMAL;
            while (_thread_running and (state != FINISH)) {
                state = target->serviceFunction();
                if (state == NOOP) usleep(_udelay);
            }
        };

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

        virtual ~ProcessThread(){
            if (_mythread != 0) {
                release(0);
                _mythread = 0;
            }
        };

        void updateDelay(float _delay) { _udelay = (__useconds_t)(_delay * 1000000); };

    private:
        boost::thread *_mythread;
        bool _thread_running;
        TargetClass *target;
        __useconds_t _udelay;
        boost::condition_variable _end_of_run;
        boost::mutex _eor_mutex;
};

class ${className} : public ${superclass}
{
/*{% for portgen in component.portgenerators if portgen.hasDeclaration() %}*/
    friend class ${portgen.className()};
/*{%   if loop.last %}*/

/*{%   endif %}*/
/*{% endfor %}*/
    public:
/*{% if component is device %}*/
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl);
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, char *compDev);
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities);
        ${className}(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities, char *compDev);
/*{% else %}*/
        ${className}(const char *uuid, const char *label);
/*{% endif %}*/

        void start() throw (CF::Resource::StartError, CORBA::SystemException);

        void stop() throw (CF::Resource::StopError, CORBA::SystemException);

/*{% if component.ports %}*/
        CORBA::Object_ptr getPort(const char* _id) throw (CF::PortSupplier::UnknownPort, CORBA::SystemException);

/*{% endif %}*/
        void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

        void initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException);

        void loadProperties();

        virtual int serviceFunction() = 0;

    protected:
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

    private:
        void construct();

};
#endif
