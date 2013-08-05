//% set classname = portgen.className()
${classname}::${classname}(std::string port_name, ${component.baseclass.name} *_parent) : 
Port_Provides_base_impl(port_name)
{
    parent = static_cast<${component.userclass.name} *> (_parent);
}

${classname}::~${classname}()
{
}
/*{% for operation in portgen.operations() %}*/

${operation.returns} ${classname}::${operation.name}(${operation.arglist})
{
    boost::mutex::scoped_lock lock(portAccess);
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
