//% set classname = portgen.className()
//% set vartype = portgen.interfaceClass() + '_var'
PREPARE_ALT_LOGGING(${classname},${component.userclass.name})
${classname}::${classname}(std::string port_name, ${component.baseclass.name} *_parent) :
Port_Uses_base_impl(port_name)
{
    parent = static_cast<${component.userclass.name} *> (_parent);
    recConnectionsRefresh = false;
    recConnections.length(0);
}

${classname}::~${classname}()
{
}
/*{% for operation in portgen.operations() %}*/

${operation.returns} ${classname}::${operation.name}(${operation.arglist})
{
//% set hasreturn = operation.returns != 'void'
/*{% if hasreturn %}*/
    ${operation.returns} retval;
/*{% endif %}*/
    std::vector < std::pair < ${vartype}, std::string > >::iterator i;

    boost::mutex::scoped_lock lock(updatingPortsLock);   // don't want to process while command information is coming in

    if (active) {
        for (i = outConnections.begin(); i != outConnections.end(); ++i) {
            try {
                ${"retval = " if hasreturn}((*i).first)->${operation.name}(${operation.argnames});
            } catch(...) {
                LOG_ERROR(${classname},"Call to ${operation.name} by ${classname} failed");
            }
        }
    }

/*{% if hasreturn %}*/
    return retval;
/*{% else %}*/
    return;
/*{% endif %}*/
}
/*{% endfor %}*/
