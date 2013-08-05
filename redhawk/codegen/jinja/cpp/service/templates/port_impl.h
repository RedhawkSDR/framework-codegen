#ifndef PORT_H
#define PORT_H

#include "ossie/Port_impl.h"
#include <queue>
#include <list>
#include <boost/thread/condition_variable.hpp>
#include <boost/thread/locks.hpp>

class ${component.baseclass.name};
class ${component.userclass.name};

#define CORBA_MAX_TRANSFER_BYTES omniORB::giopMaxMsgSize()

/*{% filter lines|unique|join('\n') %}*/
/*{% for portgen in component.portgenerators %}*/
/*{%   for header in portgen.headers() %}*/
#include ${header}
/*{%   endfor %}*/
/*{% endfor %}*/
/*{% endfilter %}*/
/*{% if "struct_props.h" in generator.sourceFiles(component) %}*/
#include "struct_props.h"
/*{% endif %}*/

/*{% if component.providesbulkio %}*/
class queueSemaphore
{
    private:
        unsigned int maxValue;
        unsigned int currValue;
        boost::mutex mutex;
        boost::condition_variable condition;

    public:
        queueSemaphore(unsigned int initialMaxValue):mutex(),condition() {
        	maxValue = initialMaxValue;
        }

        void setMaxValue(unsigned int newMaxValue) {
            boost::unique_lock<boost::mutex> lock(mutex);
            maxValue = newMaxValue;
        }

        unsigned int getMaxValue(void) {
			boost::unique_lock<boost::mutex> lock(mutex);
			return maxValue;
		}

        void setCurrValue(unsigned int newValue) {
        	boost::unique_lock<boost::mutex> lock(mutex);
        	if (newValue < maxValue) {
        		unsigned int oldValue = currValue;
        		currValue = newValue;

        		if (oldValue > newValue) {
        			condition.notify_one();
        		}
        	}
        }

        void incr() {
            boost::unique_lock<boost::mutex> lock(mutex);
            while (currValue >= maxValue) {
                condition.wait(lock);
            }
            ++currValue;
        }

        void decr() {
            boost::unique_lock<boost::mutex> lock(mutex);
            if (currValue > 0) {
            	--currValue;
            }
            condition.notify_one();
        }
};

/*{% endif %}*/
/*{% for portgen in component.portgenerators if portgen.hasDeclaration() %}*/
// ----------------------------------------------------------------------------------------
// ${portgen.className()} declaration
// ----------------------------------------------------------------------------------------
/*{% include portgen.declaration() %}*/

/*{% endfor %}*/
#endif
