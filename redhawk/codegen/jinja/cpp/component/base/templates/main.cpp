#include <iostream>
#include "ossie/ossieSupport.h"

#include "${component.userclass.header}"

/*{% if component is device %}*/
${component.userclass.name} *devicePtr;

void signal_catcher(int sig)
{
    // IMPORTANT Don't call exit(...) in this function
    // issue all CORBA calls that you need for cleanup here before calling ORB shutdown
    if (devicePtr) {
        devicePtr->halt();
    }
}
/*{% endif %}*/

int main(int argc, char* argv[])
{
/*{% if component is device %}*/
    struct sigaction sa;
    sa.sa_handler = signal_catcher;
    sa.sa_flags = 0;
    devicePtr = 0;

    Device_impl::start_device(&devicePtr, sa, argc, argv);
/*{% else %}*/
    ${component.userclass.name}* ${component.name}_servant;
    Resource_impl::start_component(${component.name}_servant, argc, argv);
/*{% endif %}*/
    return 0;
}
