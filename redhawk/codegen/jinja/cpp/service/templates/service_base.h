//% set includeGuard = component.name.upper() + '_IMPL_BASE_H'
//% set className = component.baseclass.name
//% set superclass = component.superclass.name
//% set namespace = component.namespace
//% set interface = component.interface
//% set header = component.header
#ifndef ${includeGuard}
#define ${includeGuard}

#include <boost/thread.hpp>
#include ${component.superclass.header}
#include <${header}>

class ${className} : public ${superclass}, public POA_${namespace}::${interface}
{
    public:
        ${className}(char *devMgr_ior, char *name);

        void registerServiceWithDevMgr ();
        void terminateService ();
        void construct ();

};
#endif
