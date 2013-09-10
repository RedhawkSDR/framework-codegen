//% set className = component.userclass.name
//% set baseClass = component.baseclass.name
//% set artifactType = component.artifacttype
//% set operations = component.operations
/**************************************************************************

    This is the ${artifactType} code. This file contains the child class where
    custom functionality can be added to the ${artifactType}. Custom
    functionality to the base class can be extended here. Access to
    the ports can also be done from this class

**************************************************************************/

#include "${component.userclass.header}"

PREPARE_LOGGING(${className})
${className}::${className}(char *devMgr_ior, char *name) :
    ${baseClass}(devMgr_ior, name)
{
}

${className}::~${className}()
{
}

/*{% for operation in operations %}*/
${operation.returns} ${className}::${operation.name}(${operation.arglist})
{
/*{% if operation.returns != 'void' %}*/
/*{%   if operation.returns == 'CORBA::Object_ptr' %}*/
    ${operation.returns} tmpVal = CORBA::Object::_nil();
/*{%   else %}*/
    ${operation.returns} tmpVal;
/*{%   endif %}*/
/*{% endif %}*/
    // TODO: Fill in this function
/*{% if operation.returns != 'void' %}*/
    
/*{%   if operation.returns == 'char*' %}*/
    return CORBA::string_dup(tmpVal);
/*{%   else %}*/
    return tmpVal;
/*{%   endif %}*/
/*{% endif %}*/
}

/*{% endfor %}*/
