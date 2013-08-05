//% set className = component.userclass.name
//% set baseClass = component.baseclass.name
//% set includeGuard = component.name.upper() + '_IMPL_H'
//% set operations = component.operations
#ifndef ${includeGuard}
#define ${includeGuard}

#include "${component.baseclass.header}"

class ${className};

class ${className} : public ${baseClass}
{
    ENABLE_LOGGING
    public:
        ${className}(char *devMgr_ior, char *name);
        ~${className}();
/*{% for op in operations %}*/
        ${op.returns} ${op.name}(${op.arglist});
/*{% endfor %}*/
};

#endif
