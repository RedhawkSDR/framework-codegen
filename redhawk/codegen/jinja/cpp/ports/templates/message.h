//% set className = portgen.className()
class ${className} : public MessageSupplierPort
{
    public:
        ${className}(std::string port_name) : MessageSupplierPort(port_name) {
        };
/*{% for property in component.messages %}*/
/*{%   set msgtype = property.cpptype %}*/
/*{%   set vectype = 'std::vector<'+msgtype+'>' %}*/

        void sendMessage(${msgtype} message) {
            CF::Properties outProps;
            CORBA::Any data;
            outProps.length(1);
            outProps[0].id = CORBA::string_dup(message.getId().c_str());
            outProps[0].value <<= message;
            data <<= outProps;
            push(data);
        }

        void sendMessages(${vectype|replace('>>', '> >')} messages) {
            CF::Properties outProps;
            CORBA::Any data;
            outProps.length(messages.size());
            for (unsigned int i=0; i<messages.size(); i++) {
                outProps[i].id = CORBA::string_dup(messages[i].getId().c_str());
                outProps[i].value <<= messages[i];
            }
            data <<= outProps;
            push(data);
        }
/*{% endfor %}*/
};

