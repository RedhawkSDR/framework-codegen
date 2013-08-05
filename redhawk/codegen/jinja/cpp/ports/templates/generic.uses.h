//% set classname = portgen.className()
//% set vartype = portgen.interfaceClass() + '_var'
class ${classname} : public Port_Uses_base_impl, public POA_ExtendedCF::QueryablePort
{
    ENABLE_LOGGING
    public:
        ${classname}(std::string port_name, ${component.baseclass.name} *_parent);
        ~${classname}();

/*{% for op in portgen.operations() %}*/
        ${op.returns} ${op.name}(${op.arglist});
/*{% endfor %}*/

        ExtendedCF::UsesConnectionSequence * connections() 
        {
            boost::mutex::scoped_lock lock(updatingPortsLock);   // don't want to process while command information is coming in
            if (recConnectionsRefresh) {
                recConnections.length(outConnections.size());
                for (unsigned int i = 0; i < outConnections.size(); i++) {
                    recConnections[i].connectionId = CORBA::string_dup(outConnections[i].second.c_str());
                    recConnections[i].port = CORBA::Object::_duplicate(outConnections[i].first);
                }
                recConnectionsRefresh = false;
            }
            ExtendedCF::UsesConnectionSequence_var retVal = new ExtendedCF::UsesConnectionSequence(recConnections);
            // NOTE: You must delete the object that this function returns!
            return retVal._retn();
        };

        void connectPort(CORBA::Object_ptr connection, const char* connectionId)
        {
            boost::mutex::scoped_lock lock(updatingPortsLock);   // don't want to process while command information is coming in
            ${vartype} port = ${portgen.interfaceClass()}::_narrow(connection);
            outConnections.push_back(std::make_pair(port, connectionId));
            active = true;
            recConnectionsRefresh = true;
        };

        void disconnectPort(const char* connectionId)
        {
            boost::mutex::scoped_lock lock(updatingPortsLock);   // don't want to process while command information is coming in
            for (unsigned int i = 0; i < outConnections.size(); i++) {
                if (outConnections[i].second == connectionId) {
                    outConnections.erase(outConnections.begin() + i);
                    break;
                }
            }

            if (outConnections.size() == 0) {
                active = false;
            }
            recConnectionsRefresh = true;
        };

        std::vector< std::pair<${vartype}, std::string> > _getConnections()
        {
            return outConnections;
        };

    protected:
        ${component.userclass.name} *parent;
        std::vector < std::pair<${vartype}, std::string> > outConnections;
        ExtendedCF::UsesConnectionSequence recConnections;
        bool recConnectionsRefresh;
};
